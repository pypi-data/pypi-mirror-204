# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# TODO: in need of refactoring

import base64
import datetime
import io
from pathlib import Path
from time import time

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yaml
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output, State
from dash.development.base_component import Component

from optimization_problem_inspector import (
    features,
    problem,
    sampling,
    serialization,
)
from optimization_problem_inspector.app_strings import (
    REFERENCE_BBOB_NAMES,
    TEXT,
)
from optimization_problem_inspector.config import (
    FEAT_CALCULATION_TIME_WARN_THRESHOLD_S,
    PLOT_HEIGHT_MULTIPLIER,
    PLOT_HEIGHT_STATIC_DEFAULT,
    PLOT_MARGIN,
    PLOT_WIDTH_MULTIPLIER,
)
from optimization_problem_inspector.logger import logger

DEFAULT_PROBLEM_ARGS = {
    "dim": 5,
    "obj": 2,
    "fi": 1,
    "instance": 3,
}
"""Default simplified GBBOB problem specification
to show on the first loading of the app.
"""

DEFAULT_SAMPLE_SIZE = 100
"""Default sample size to use when sampling
"""
DEFAULT_SAMPLING_SEED = 42
"""Default sample seed to use when sampling
"""

DEFAULT_PROBLEM = problem.GBBOBProblemFactory(
    problem.make_simple_gbbob_defn(
        dimensions=DEFAULT_PROBLEM_ARGS["dim"],
        objectives=DEFAULT_PROBLEM_ARGS["obj"],
        fi=DEFAULT_PROBLEM_ARGS["fi"],
        instance_offset=DEFAULT_PROBLEM_ARGS["instance"],
    ),
)
"""Default simplified GBBOB problem to use when first
loading the app
"""


def get_default_sampling_parameters(
    default_seed: int = DEFAULT_SAMPLING_SEED,
) -> str:
    """Generate default sampling parameters.

    Args:
        default_seed (int, optional): Seed to use with sampling.
            Defaults to DEFAULT_SAMPLING_SEED.

    Returns:
        str: Serialized dictionary of sampling parameters for all
            registered sampling methods.
    """
    return yaml.dump(
        {
            s.__name__: {"random_seed": default_seed}
            for s in sampling.OPI_SAMPLERS
        }
    )


def load_sampling_parameters(parameters_dump: str) -> dict:
    """Deserialize sampling parameters for each sampling method.

    Args:
        parameters_dump (str): Serialized parameters

    Raises:
        ValueError: Could not deserialize sampling parameters

    Returns:
        dict: Sampling parameters for each sampling method
    """
    with io.StringIO(parameters_dump) as pd:
        sp = yaml.safe_load(pd)
    available = {s.__name__ for s in sampling.OPI_SAMPLERS}
    extra = []
    for p in sp:
        if p not in available:
            extra.append(p)
    if extra:
        logger.warning(f"Samplers {extra = }")
        raise ValueError(f"Unknown samplers defined: {extra}")
    return sp


def get_help_text() -> str:
    """Load GUI help text from assets/gui-help.md file and format
    certain strings with dynamic text.

    Returns:
        str: GUI help text with formatted dynamic text inputs.
    """
    help_file = Path(__file__).parent / "assets" / "gui-help.md"

    with help_file.open() as f:
        help_text = f.read()

    return help_text.format(
        APP_NAME=TEXT.APP_NAME,
    )


app = Dash(
    __name__, title=TEXT.APP_NAME, external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children=TEXT.APP_NAME),
            ],
            style={
                "margin": "10px",
            },
        ),
        html.Hr(),
        html.Details(
            children=[
                html.Summary(children=TEXT.SEC_PROBLEM_SPECIFICATION),
                html.Div(
                    [
                        dcc.Upload(
                            id="upload-problem-spec",
                            children=html.Div(
                                [TEXT.DRAG_AND_DROP_OR_SELECT_FILES]
                            ),
                            style={
                                "width": "calc(100% - 22px)",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px",
                            },
                            # Allow multiple files to be uploaded
                            multiple=False,
                            className="upload-box",
                        ),
                        html.Div(id="output-data-upload"),
                    ],
                    style={
                        "margin": "10px",
                    },
                ),
            ],
            style={
                "margin": "10px",
            },
        ),
        html.Hr(),
        html.Details(
            children=[
                html.Summary(children=TEXT.SEC_SAMPLE_GENERATION),
                html.Div(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [
                                        html.Pre(
                                            html.Code(
                                                dcc.Textarea(
                                                    id="sampling-parameters",
                                                    value=get_default_sampling_parameters(),  # noqa E501
                                                    style={
                                                        "width": "100%",
                                                        "height": 300,
                                                    },
                                                ),
                                            )
                                        )
                                    ],
                                    title=TEXT.SEC_SAMPLE_GENERATION_PARAMETERS,  # noqa E501
                                ),
                            ],
                            start_collapsed=True,
                        ),
                        dbc.Label(TEXT.SEC_SAMPLE_GENERATION_METHOD),
                        dbc.Select(
                            [s.__name__ for s in sampling.OPI_SAMPLERS],
                            "RandomSampler",
                            id="sample-generation-method-select",
                        ),
                        html.Div(
                            id="sample-generation-method-arguments",
                            style={
                                "margin": "10px",
                            },
                        ),
                        dbc.Label(TEXT.SEC_SAMPLE_GENERATION_PARAM_N),
                        dbc.Input(
                            value=DEFAULT_SAMPLE_SIZE,
                            id="sample-generation-N-select",
                            type="number",
                            placeholder="N",
                        ),
                        html.Div(
                            [
                                dbc.Button(
                                    TEXT.SAMPLE_GENERATION_BUTTON,
                                    id="btn-download-txt",
                                ),
                                dcc.Download(id="download-text"),
                            ]
                        ),
                    ],
                    style={
                        "margin": "10px",
                    },
                ),
            ],
            style={
                "margin": "10px",
            },
        ),
        html.Hr(),
        html.Details(
            children=[
                html.Summary(children=TEXT.SEC_DATA),
                html.Div(
                    [
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div(
                                [TEXT.DRAG_AND_DROP_OR_SELECT_FILES]
                            ),
                            style={
                                "width": "calc(100% - 22px)",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px",
                            },
                            # Allow multiple files to be uploaded
                            multiple=False,
                            className="upload-box",
                        ),
                        html.Div(id="upload-data-alerting"),
                        html.Div(
                            id="data-table-container",
                            children=[
                                dash_table.DataTable(
                                    id="data-table", page_size=50
                                )
                            ],
                        ),
                    ],
                    style={
                        "margin": "10px",
                    },
                ),
            ],
            style={
                "margin": "10px",
            },
        ),
        html.Hr(),
        html.Details(
            children=[
                html.Summary(children=TEXT.SEC_REFERENCE_PROBLEMS),
                html.Div(id="reference-container-alerting"),
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                html.Pre(
                                    html.Code(
                                        dcc.Textarea(
                                            id="reference-problem-definitions",
                                            value="",
                                            style={
                                                "width": "100%",
                                                "height": 300,
                                            },
                                        ),
                                    )
                                )
                            ],
                            title=TEXT.REF_PROBLEM_DEFINITIONS_LABEL,
                        ),
                        dbc.AccordionItem(
                            [
                                html.Pre(
                                    html.Code(
                                        dcc.Textarea(
                                            id="features-parameters",
                                            value="",
                                            style={
                                                "width": "100%",
                                                "height": 300,
                                            },
                                        ),
                                    )
                                )
                            ],
                            title=TEXT.SEC_REF_FEATURES_PARAMETERS,
                        ),
                    ],
                    start_collapsed=True,
                ),
                dbc.Label(
                    TEXT.SEC_REF_FEATURES_SELECT,
                    style={
                        "margin": "10px",
                    },
                ),
                dcc.Dropdown(
                    id="reference-feature-selection",
                    multi=True,
                    options=[f.__name__ for f in features.FEATURES_LIST],
                    value=[
                        f.__name__
                        for f in features.FEATURES_LIST
                        if not (
                            f.__name__.endswith("_N") or "neigh" in f.__name__
                        )
                    ],
                ),
                dcc.Loading(
                    id="reference-container-loading",
                    children=[
                        html.Div(
                            [
                                html.Div(id="reference-container"),
                            ],
                        ),
                    ],
                    style={
                        "margin": "10px",
                    },
                ),
            ],
            open=True,
            style={
                "margin": "10px",
            },
        ),
        html.Hr(),
        html.Details(
            children=[
                html.Summary(children=TEXT.SEC_VIZUALIZATION),
                html.Div(
                    [
                        dbc.Select(
                            ["scatter_matrix", "parallel_coordinates"],
                            "scatter_matrix",
                            id="visualization-method-select",
                        ),
                        dbc.Label(TEXT.SEC_VIZUALIZATION_DIMENSION_SELECT),
                        dcc.Dropdown(
                            id="visualization-plot-options-columns",
                            multi=True,
                        ),
                        dbc.Label(TEXT.SEC_VIZUALIZATION_COLOR_SELECT),
                        dcc.Dropdown(
                            id="visualization-plot-options-color",
                            multi=False,
                        ),
                        dcc.Loading(
                            id="visualization-container-loading",
                            children=[
                                html.Div(
                                    [
                                        html.Div(id="visualization-container"),
                                    ],
                                ),
                            ],
                            style={
                                "margin": "10px",
                            },
                        ),
                    ],
                    style={
                        "margin": "10px",
                    },
                ),
            ],
            open=True,
            style={
                "margin": "10px",
            },
        ),
        html.Hr(),
        html.Details(
            children=[
                html.Summary(children=TEXT.SEC_HELP),
                dcc.Markdown(
                    get_help_text(),
                    style={
                        "margin": "10px",
                    },
                ),
            ],
            open=False,
            style={
                "margin": "10px",
            },
        ),
        html.Footer(
            children=[
                html.Hr(),
                dcc.Markdown(children=TEXT.FOOTNOTE),
            ],
            style={
                # "position": "fixed",
                "width": "100%",
                "bottom": "5px",
                "textAlign": "center",
                "color": "darkgray",
            },
        ),
        dcc.Store(id="problem-specification"),
    ]
)


def file_to_html_elements(contents, filename, dt):
    return html.Div(
        [
            html.H5(filename),
            html.Pre(
                contents,
                style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
            ),
        ]
    )


@app.callback(
    Output("output-data-upload", "children"),
    Output("problem-specification", "data"),
    Input("upload-problem-spec", "contents"),
    State("upload-problem-spec", "filename"),
    State("upload-problem-spec", "last_modified"),
)
def update_problem_specification_output(contents, filename, dt):
    decoded = None
    if contents is None:
        dim = DEFAULT_PROBLEM_ARGS["dim"]
        obj = DEFAULT_PROBLEM_ARGS["obj"]
        fi = DEFAULT_PROBLEM_ARGS["fi"]
        common_name = REFERENCE_BBOB_NAMES[fi]
        filename = (
            f"BBOB__dim_{dim}__obj_{obj}__fo_{fi}__{common_name}"
            ".optimization_problem_inspector.yaml"
        )
        # TODO: may have to improve this
        dt = datetime.datetime.now()
        decoded = serialization.dumps_spec(DEFAULT_PROBLEM.spec)
    else:
        _, content_string = contents.split(",")
        decoded = base64.b64decode(content_string).decode("utf-8")

    if decoded is not None:
        children = [file_to_html_elements(decoded, filename, dt)]
    else:
        return None, None

    return (children, decoded)


@app.callback(
    Output("data-table", "data"),
    Output("data-table", "columns"),
    Output("upload-data-alerting", "children"),
    Output("reference-container-alerting", "children"),
    Input("upload-problem-spec", "contents"),
    Input("upload-data", "contents"),
    Input("sample-generation-N-select", "value"),
    Input("sample-generation-method-select", "value"),
    Input("sampling-parameters", "value"),
)
def update_data_in_problem_data_table(
    spec_contents,
    data_contents,
    sample_n,
    sample_method_name,
    sampling_parameters_dump,
):
    if spec_contents is None:
        specs = DEFAULT_PROBLEM.spec
    else:
        _, spec_content_string = spec_contents.split(",")
        spec_decoded = base64.b64decode(spec_content_string).decode("utf-8")
        with io.StringIO(spec_decoded) as f:
            specs = serialization.load_spec(f)
    spec_columns = specs.get_columns()
    sampling_parameters = load_sampling_parameters(sampling_parameters_dump)

    df = None
    if data_contents is None:
        sample_generation_method = getattr(sampling, sample_method_name)
        problem_data = DEFAULT_PROBLEM.get_problem_sample(
            sampler=sample_generation_method,
            N=sample_n,
            sampler_kwargs=sampling_parameters.get(sample_method_name),
        )
        df = problem_data.data
        # return (None, None)
    else:
        _, content_string = data_contents.split(",")
        decoded = base64.b64decode(content_string).decode("utf-8")
        with io.StringIO(decoded) as f:
            df = pd.read_csv(f)

    alert_div = None
    if df is not None:
        if df.columns.to_list() != spec_columns:
            msg = f"Mismatch {df.columns.to_list() = } <> {spec_columns = }"
            alert_div = dbc.Alert(
                msg,
                color="danger",
            )
            logger.warning(msg)
        logger.debug(df.to_csv(index=False))
        return (
            df.to_dict("records"),
            [{"name": i, "id": i} for i in df.columns],
            alert_div,
            alert_div,
        )
    else:
        return None, None, None, None


@app.callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    State("sample-generation-N-select", "value"),
    State("sample-generation-method-select", "value"),
    State("problem-specification", "data"),
    State("sampling-parameters", "value"),
    prevent_initial_call=True,
)
def generate_problem_sample_file(
    n_clicks,
    N,
    sample_generation_method_name,
    spec_contents,
    sampling_parameters_dump,
):
    logger.debug(spec_contents)
    with io.StringIO(spec_contents) as f:
        specs = serialization.load_spec(f)

    sample_generation_method = getattr(sampling, sample_generation_method_name)
    sampling_parameters = load_sampling_parameters(sampling_parameters_dump)
    selected_sampling_params = sampling_parameters.get(
        sample_generation_method_name
    )
    if selected_sampling_params is None:
        selected_sampling_params = {}
    sampler = sampling.OPISamplerFactory(
        sample_generation_method, specs, **selected_sampling_params
    )
    sample = sampler.sample(N)
    return dict(content=sample.to_csv(index=False), filename="data.csv")


@app.callback(
    Output("reference-problem-definitions", "value"),
    Input("problem-specification", "data"),
)
def update_reference_problem_specs(problem_spec):
    objs = problem_spec.count("OBJECTIVES")
    dims = problem_spec.count("VARIABLES")
    constraints = problem_spec.count("CONSTRAINTS")
    ref_problems = problem.ReferenceProblemsGBBOB.from_simple_input(
        dimensions=dims, objectives=objs, constraints=constraints
    )
    ref_problems_dump = ref_problems.dumps()
    return ref_problems_dump


@app.callback(
    Output("features-parameters", "value"),
    Input("problem-specification", "data"),
)
def update_feature_parameters(problem_spec):
    feature_parameters = {}
    feature_parameters[features.neighbourhood_feats.__name__] = {
        "number_neighbours": 10
    }
    return yaml.dump(feature_parameters)


def load_feature_parameters(feature_parameters_dump: str) -> dict:
    """Deserialize feature parameters.

    Args:
        feature_parameters_dump (str): Serialized feature parameters.

    Raises:
        ValueError: Could not deserialize feature parameters.

    Returns:
        dict: Feature name to feature parameters mapping
    """
    with io.StringIO(feature_parameters_dump) as f:
        feature_parameters = yaml.safe_load(f)
    extra = []
    available_features = {f.__name__ for f in features.FEATURES_LIST}
    for f in feature_parameters:
        if f not in available_features:
            extra.append(f)
    if len(extra) > 0:
        logger.warning(f"{extra = }")
        raise ValueError(f"Unknown features defined: {extra}")
    return feature_parameters


@app.callback(
    Output("reference-container", "children"),
    Input("data-table", "data"),
    Input("reference-problem-definitions", "value"),
    Input("features-parameters", "value"),
    State("problem-specification", "data"),
    State("sample-generation-N-select", "value"),
    State("sample-generation-method-select", "value"),
    State("sampling-parameters", "value"),
    Input("reference-feature-selection", "value"),
)
def update_reference_problems_and_features(
    problem_data,
    ref_problem_definitions,
    feature_parameters_dump,
    problem_spec,
    n,
    sample_method_name,
    sampling_parameters_dump,
    feature_list_names,
):
    features_to_use = [getattr(features, f) for f in feature_list_names]
    df = pd.DataFrame(problem_data)
    logger.debug(f"{df.shape = }")
    try:
        spec = serialization.load_spec(problem_spec)
    except Exception as e:
        raise ValueError(
            f"Could not load specification because {type(e).__name__}: {e}."
            " Is the specification format correct?"
        )
    try:
        ref_problems = problem.ReferenceProblemsGBBOB.loads(
            ref_problem_definitions
        )
    except Exception as e:
        raise ValueError(
            "Could not load reference problems because"
            f" {type(e).__name__}: {e}. Is the specification format correct?"
        )
    feature_parameters = load_feature_parameters(feature_parameters_dump)

    this_data_feature_makers = []
    for feature_to_use in features_to_use:
        ff_params = feature_parameters.get(feature_to_use.__name__)
        if ff_params is None:
            ff_params = {}
        ff = features.OPIFeatureFactory(feature_to_use, spec, **ff_params)
        this_data_feature_makers.append(ff)

    this_feats = {}
    short_to_long_names_mapper = {}
    for this_data_feature_maker in this_data_feature_makers:
        for k, v in this_data_feature_maker.compute(df=df).items():
            this_feats[k] = v
        short_to_long_names_mapper = {
            **short_to_long_names_mapper,
            **getattr(this_data_feature_maker, "short_to_long_names", {}),
        }

    sample_generation_method = getattr(sampling, sample_method_name)
    sampling_parameters = load_sampling_parameters(sampling_parameters_dump)
    selected_sampling_params = sampling_parameters.get(
        sample_generation_method
    )
    samples = ref_problems.get_problem_samples(
        sample_generation_method, N=n, sampler_kwargs=selected_sampling_params
    )

    def get_function_index(problem):
        try:
            fi = int(problem.name.split("__")[-1].replace("fi_", ""))
            logger.info(f"{problem.name = } -> {fi}")
            return fi
        except ValueError:
            for i in range(24):
                if f"f{i}_" in problem.name:
                    logger.info(f"{problem.name = } -> {i}")
                    return i

            logger.info(f"{problem.name = } -> {None}")

    feats = []
    for problem_data in samples:
        for feature_to_use in features_to_use:
            tic = time()
            function_index = get_function_index(problem_data.problem)
            problem_name = problem_data.problem.name
            fm = features.OPIFeatureFactory(
                feature_to_use, problem_data.problem.spec
            )
            feats.append(
                {
                    "features": fm.compute(problem_data.data),
                    "problem_name": problem_name,
                    "function_index": function_index,
                }
            )
            toc = time()
            duration = toc - tic
            if duration > FEAT_CALCULATION_TIME_WARN_THRESHOLD_S:
                log_method = logger.warning
            else:
                log_method = logger.info
            log_method(
                f"{type(fm).__name__} on problem {problem_name}"
                f" took {duration:.4f}s"
            )

    rows = []
    rows_data = []

    for k, v in this_feats.items():
        rows_data.append(
            (
                0,  # function index
                TEXT.REF_PROBLEM_THIS_PROBLEM_NAME,
                k,
                v,
            )
        )
        rows.append(
            html.Tr(
                [
                    html.Td(html.B(TEXT.REF_PROBLEM_THIS_PROBLEM_NAME)),
                    html.Td(html.B(k)),
                    html.Td(html.B(f"{v}")),
                ]
            )
        )

    for feature_d in feats:
        problem_name = feature_d["problem_name"]
        function_index = feature_d["function_index"]
        for k, v in feature_d["features"].items():
            rows.append(
                html.Tr(
                    [
                        html.Td(problem_name),
                        html.Td(k),
                        html.Td(f"{v}"),
                    ]
                )
            )
            rows_data.append(
                (
                    function_index,
                    problem_name,
                    k,
                    v,
                )
            )

    def html_rows_sorter(row):
        try:
            return (
                row.children[1].children,
                float(row.children[2].children),
                row.children[0].children,
            )
        except Exception:
            return (
                row.children[1].children.children,
                float(row.children[2].children.children),
                row.children[0].children.children,
            )

    def data_rows_sorter(row):
        return (row[1], row[2], row[0])

    rows = sorted(
        rows,
        key=html_rows_sorter,
    )
    problem_id_column = "problem_id"
    problem_name_id = "problem_name_id"
    rows_data = sorted(rows_data, key=data_rows_sorter)
    rows_data_long = pd.DataFrame(
        rows_data,
        columns=[
            problem_id_column,
            TEXT.REF_PROBLEM_TABLE_PROBLEM_NAME,
            TEXT.REF_PROBLEM_TABLE_FEATURE_NAME,
            TEXT.REF_PROBLEM_TABLE_FEATURE_VALUE,
        ],
    )
    rows_data_long[TEXT.REF_PROBLEM_TABLE_FEATURE_NAME] = rows_data_long[
        TEXT.REF_PROBLEM_TABLE_FEATURE_NAME
    ].apply(lambda x: short_to_long_names_mapper.get(x, x))

    # we have to pivot the features table to be able to plot
    # same features on the same parallel coordinate
    rows_data_wide = pd.pivot_table(
        data=rows_data_long,
        values=TEXT.REF_PROBLEM_TABLE_FEATURE_VALUE,
        columns=[TEXT.REF_PROBLEM_TABLE_FEATURE_NAME],
        index=(problem_id_column, TEXT.REF_PROBLEM_TABLE_PROBLEM_NAME),
    ).reset_index()
    problem_names_unq = sorted(
        pd.unique(rows_data_wide[TEXT.REF_PROBLEM_TABLE_PROBLEM_NAME]).tolist()
    )
    problem_names_map = {
        n: i + 1
        for i, n in enumerate(problem_names_unq)
        if n != TEXT.REF_PROBLEM_THIS_PROBLEM_NAME
    }
    problem_names_map[TEXT.REF_PROBLEM_THIS_PROBLEM_NAME] = 0
    rows_data_wide[problem_name_id] = rows_data_wide[
        TEXT.REF_PROBLEM_TABLE_PROBLEM_NAME
    ].map(problem_names_map)
    feature_cols = [
        c
        for c in rows_data_wide.columns
        if c
        not in [
            TEXT.REF_PROBLEM_TABLE_PROBLEM_NAME,
            TEXT.REF_PROBLEM_TABLE_FEATURE_NAME,
            TEXT.REF_PROBLEM_TABLE_FEATURE_VALUE,
            problem_id_column,
            problem_name_id,
        ]
    ]
    dimensions = []
    dimensions.append(
        {
            "range": [
                rows_data_wide[problem_name_id].min(),
                rows_data_wide[problem_name_id].max(),
            ],
            "label": TEXT.REF_PROBLEM_TABLE_PROBLEM_NAME,
            "values": rows_data_wide[problem_name_id],
            "tickvals": rows_data_wide[problem_name_id],
            "ticktext": rows_data_wide[TEXT.REF_PROBLEM_TABLE_PROBLEM_NAME],
        }
    )
    dimensions.extend(
        [
            {
                "range": [rows_data_wide[c].min(), rows_data_wide[c].max()],
                "label": c,
                "values": rows_data_wide[c],
            }
            for c in feature_cols
        ]
    )
    fig = go.Figure(
        data=go.Parcoords(
            line={
                "color": rows_data_wide[problem_name_id],
                "colorscale": px.colors.diverging.Portland,
            },
            dimensions=dimensions,
        )
    )
    max_name = max([len(n) for n in problem_names_map])
    fig.update_layout(
        autosize=False,
        width=(len(rows_data_wide.columns) - 1) * PLOT_WIDTH_MULTIPLIER / 2
        + PLOT_MARGIN,
        height=PLOT_HEIGHT_STATIC_DEFAULT,  # , // 2,
        margin=go.layout.Margin(l=max_name * 5),
    )
    return [
        html.Div(
            [
                dcc.Graph(
                    figure=fig,
                ),
                generate_download_button(
                    fig=fig, fig_id="visualize-references"
                ),
            ],
            id="reference-container-plot",
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dbc.Table(
                            [
                                html.Thead(
                                    html.Tr(
                                        [
                                            html.Th(
                                                TEXT.REF_PROBLEM_TABLE_PROBLEM_NAME  # noqa E501
                                            ),
                                            html.Th(
                                                TEXT.REF_PROBLEM_TABLE_FEATURE_NAME  # noqa E501
                                            ),
                                            html.Th(
                                                TEXT.REF_PROBLEM_TABLE_FEATURE_VALUE  # noqa E501
                                            ),
                                        ]
                                    )
                                ),
                                html.Tbody(rows),
                            ],
                            bordered=True,
                        ),
                    ],
                    title=TEXT.REF_PROBLEM_TABLE_NAME,  # noqa E501
                ),
            ],
            start_collapsed=True,
        ),
        get_data_download_button(rows_data_long, data_id="reference-values"),
    ]


@app.callback(
    Output("visualization-plot-options-columns", "options"),
    Output("visualization-plot-options-columns", "value"),
    Output("visualization-plot-options-color", "options"),
    Output("visualization-plot-options-color", "value"),
    Input("data-table", "data"),
)
def update_plot_options_columns(problem_data):
    df = pd.DataFrame(problem_data)
    values = df.columns.to_list()
    return values, values, values, values[-1]


def get_html_figure_encoded(fig: go.Figure) -> str:
    """Generate base64 encoded html export of the plotly figure.

    We need this so we can inline the whole html document in the button link.

    Args:
        fig (go.Figure): Plotly figure to export

    Returns:
        str: Base64 encoded html export of plotly figure.
    """
    buffer = io.StringIO()
    fig.write_html(buffer)
    html_bytes = buffer.getvalue().encode()
    encoded = base64.b64encode(html_bytes).decode()
    return encoded


def get_data_download_button(data_df: pd.DataFrame, data_id: str) -> Component:
    """Generate a dash button to download data_df as csv.

    Args:
        data_df (pd.DataFrame): DataFrame to download
        data_id (str): Id of the download button

    Returns:
        Component: Dash component to download the data
    """
    b64_encoded = base64.b64encode(
        data_df.to_csv(index=False).encode()
    ).decode()
    return html.A(
        dbc.Button(TEXT.DOWNLOAD_DATA_AS_CSV_BUTTON, color="link"),
        id=data_id,
        href="data:text/csv;base64," + b64_encoded,
        download=f"data_{data_id}.csv",
    )


def generate_download_button(fig: go.Figure, fig_id: str) -> Component:
    """Generate a dash button to download figure export as HTML.

    Args:
        fig (go.Figure): Plotly figure to download
        fig_id (str): Id of the download button

    Returns:
        Component: Dash component to download the data
    """
    return html.A(
        dbc.Button(TEXT.DOWNLOAD_FIGURE_AS_HTML_BUTTON, color="link"),
        id=fig_id,
        href="data:text/html;base64," + get_html_figure_encoded(fig=fig),
        download=f"plotly_graph_{fig_id}.html",
    )


@app.callback(
    Output("visualization-container", "children"),
    Input("visualization-method-select", "value"),
    Input("data-table", "data"),
    Input("visualization-plot-options-columns", "value"),
    Input("visualization-plot-options-color", "value"),
)
def update_plot(
    plot_method, problem_data, visualization_plot_options_columns, color_column
):
    logger.debug(f"{plot_method = }")
    df = pd.DataFrame(problem_data)
    ordered_columns = [
        c for c in df.columns if c in visualization_plot_options_columns
    ]
    logger.debug(f"{df.shape = }")
    if plot_method == "parallel_coordinates":
        fig_height = PLOT_HEIGHT_STATIC_DEFAULT
    else:
        fig_height = (
            len(ordered_columns) * PLOT_HEIGHT_MULTIPLIER + PLOT_MARGIN
        )
    plot_method = getattr(px, plot_method)
    fig = plot_method(
        df,
        dimensions=ordered_columns,
        width=len(ordered_columns) * PLOT_WIDTH_MULTIPLIER + PLOT_MARGIN,
        height=fig_height,
        color=color_column,
    )

    return [
        dcc.Graph(figure=fig),
        generate_download_button(fig=fig, fig_id="visualize-data"),
    ]


def main():
    logger.info("Starting server...")
    # we need host="0.0.0.0" (all interfaces) to support serving
    # the application in docker
    # TODO: maybe make configurable from the CLI
    app.run_server(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
