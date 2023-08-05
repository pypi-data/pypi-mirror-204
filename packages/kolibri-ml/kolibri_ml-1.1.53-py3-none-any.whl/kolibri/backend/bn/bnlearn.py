import numpy as np
import pandas as pd
from kolibri.backend.bn.metrics import structure_score
import itertools
from tabulate import tabulate
from decimal import Decimal
from kolibri.backend.bn.BayesianNetwork import BayesianNetwork
from kolibri.backend.bn.NaiveBayes import NaiveBayes
import networkx as nx
from kolibri.backend.bn import network
import os
import matplotlib.pyplot as plt

# %% Get node properties
def get_node_properties(model, node_color='#1f456e', node_size=None, verbose=3):
    """Collect node properties.

    Parameters
    ----------
    model : dict
        dict containing (initialized) model.
    node_color : str, (Default: '#000000')
        The default color of the edges.
    node_size : float, (Default: 1)
        The default weight of the edges.
    Print progress to screen. The default is 3.
        0: None, 1: ERROR, 2: WARN, 3: INFO (default), 4: DEBUG, 5: TRACE

    Returns
    -------
    dict.
        Node properties.

    Examples
    --------


    """
    # https://networkx.org/documentation/networkx-1.7/reference/generated/networkx.drawing.nx_pylab.draw_networkx_nodes.html
    nodes = {}
    defaults={'node_color': node_color, 'node_size': node_size}
    adjmat = model.get('adjmat', None)

    if adjmat is not None:
        if verbose>=3: print('[bnlearn] >Set node properties.')
        # For each node, use the default node properties.
        for node in adjmat.columns:
            node_property = defaults.copy()
            nodes.update({node: node_property})

    # Return dict with node properties
    return nodes


# %% Get node properties
def get_edge_properties(model, color='#000000', weight=1, minscale=1, maxscale=10, verbose=3):
    """Collect edge properties.

    Parameters
    ----------
    model : dict
        dict containing (initialized) model.
    color : str, (Default: '#000000')
        The default color of the edges.
    weight : float, (Default: 1)
        The default weight of the edges.
    minscale : float, (Default: 1)
        The minimum weight of the edge in case of test statisics are used.
    maxscale : float, (Default: 10)
        The maximum weight of the edge in case of test statisics are used.
    verbose : int, optional
        Print progress to screen. The default is 3.
        0: None, 1: ERROR, 2: WARN, 3: INFO (default), 4: DEBUG, 5: TRACE

    Returns
    -------
    dict.
        Edge properties.

    Examples
    --------

    """
    # https://networkx.org/documentation/networkx-1.7/reference/generated/networkx.drawing.nx_pylab.draw_networkx_nodes.html
    edges = {}
    defaults = {'color': color, 'weight': weight}
    adjmat = model.get('independence_test', None)
    # Use edge weights from test statistic
    if adjmat is not None:
        if verbose>=3: print('[bnlearn]> Set edge weights based on the [%s] test statistic.' %(model['independence_test'].columns[-2]))
        logp = -np.log10(model['independence_test']['p_value'])
        logp[np.isinf(logp)] = logp[np.isfinite(logp)].max()
        weights = _normalize_weights(logp.values, minscale=minscale, maxscale=maxscale)
        adjmat = vec2adjmat(model['independence_test']['source'], model['independence_test']['target'], weights=weights)
    else:
        adjmat = model.get('adjmat', None)

    # Get model edges
    model_edges = adjmat2vec(adjmat)[['source', 'target']].values
    # model_edges = model['model'].edges() if (model.get('model_edges', None) is None) else model['model_edges']

    # Store edge properties
    if adjmat is not None:
        if verbose>=3: print('[bnlearn] >Set edge properties.')
        # For each edge, use the default properties.
        for u, v in model_edges:
            edge_property = defaults.copy()
            # Use the edge weight from the adjmat
            if not isinstance(adjmat.loc[u, v], np.bool_):
                edge_property['weight']=adjmat.loc[u, v]
            # Update edges dict
            edges.update({(u, v): edge_property})

    # Return dict with node properties
    return edges


# %% Normalize weights in range
def _normalize_weights(weights, minscale=1, maxscale=10):
    if len(weights.shape)==1:
        weights=weights.reshape(-1, 1)

    from sklearn.preprocessing import MinMaxScaler
    weights = MinMaxScaler(feature_range=(minscale, maxscale)).fit_transform(weights).flatten()
    return(weights)

# %% Plot properties
def _plot_properties(G, node_properties, edge_properties, node_color, node_size):
    # Set edge properties in Graph G
    # edges=[*bnmodel.edges()]
    edges = list(edge_properties.keys())
    for edge in edges:
        color = edge_properties.get((edge[0], edge[1])).get('color', '#000000')
        weight = edge_properties.get((edge[0], edge[1])).get('weight', 1)
        G.add_edge(edge[0], edge[1], weight=weight, color=color)
        # arrowstyle = edge_properties.get((edge[0], edge[1])).get('arrowstyle', '-|>')
        # arrowsize = edge_properties.get((edge[0], edge[1])).get('arrowsize', 30)
        # G.add_edge(edge[0], edge[1], weight=weight, color=color, arrowstyle=arrowstyle, arrowsize=arrowsize)

    edgelist = list(G.edges())
    edge_colors = [G[u][v].get('color') for u, v in G.edges()]
    edge_weights = [G[u][v].get('weight') for u, v in G.edges()]
    # edge_arrowstyles = [G[u][v].get('arrowstyle') for u, v in G.edges()]
    # edge_arrowsizes = [G[u][v].get('arrowsize') for u, v in G.edges()]

    # Node properties
    nodelist = np.unique(edgelist)
    node_colors = []
    node_sizes = []
    for node in nodelist:
        if node_color is not None:
            node_colors.append(node_color)
        else:
            node_colors.append(node_properties[node].get('node_color'))
        if node_size is not None:
            node_sizes.append(node_size)
        else:
            node_sizes.append(node_properties[node].get('node_size'))
    # Return
    return nodelist, node_colors, node_sizes, edgelist, edge_colors, edge_weights



# %% PLOT
def plot(model,
         pos=None,
         scale=1,
         interactive=False,
         title='bnlearn_causal_network',
         node_color=None,
         node_size=None,
         node_properties=None,
         edge_properties=None,
         params_interactive={'width': '70%', 'height': '800px', 'notebook': False, 'layout': None, 'font_color': False, 'bgcolor': '#ffffff', 'select_menu': True, 'filter_menu': True, 'cdn_resources': 'remote'},
         params_static={'minscale': 1, 'maxscale': 10, 'figsize': (15, 10), 'width': None, 'height': None, 'font_size': 14, 'font_family': 'sans-serif', 'alpha': 0.8, 'node_shape': 'o', 'layout': 'spring_layout', 'font_color': '#000000', 'facecolor': 'white', 'edge_alpha': 0.8, 'arrowstyle': '-|>', 'arrowsize': 30, 'visible': True},
         verbose=3):
    """Plot the learned stucture.

    Parameters
    ----------
    model : dict
        Learned model from the .fit() function.
    pos : graph, optional
        Coordinates of the network. If there are provided, the same structure will be used to plot the network.. The default is None.
    scale : int, optional
        Scaling parameter for the network. A larger number will linearily increase the network.. The default is 1.
    interactive : Bool, (default: True)
        True: Interactive web-based graph.
        False: Static plot
    title : str, optional
        Title for the plots.
    node_color : str, optional
        Color each node in the network using a hex-color, such as '#8A0707'
    node_size : int, optional
        Set the node size for each node in the network. The default size when using static plolts is 800, and for interactive plots it is 10.
    node_properties : dict (default: None)
        Dictionary containing custom node_color and node_size parameters for the network.
        The node properties can easily be retrieved using the function: node_properties = bn.get_node_properties(model)
        node_properties = {'node1':{'node_color':'#8A0707','node_size':10},
                           'node2':{'node_color':'#000000','node_size':30}}
    edge_properties : dict (default: None).
        Dictionary containing custom node_color and node_size parameters for the network. The edge properties can be retrieved with:
        edge_properties = bn.get_edge_properties(model)
    params_interactive : dict.
        Dictionary containing various settings in case of creating interactive plots.
    params_static : dict.
        Dictionary containing various settings in case of creating static plots.
        layout: 'spring_layout', 'planar_layout', 'shell_layout', 'spectral_layout', 'pydot_layout', 'graphviz_layout', 'circular_layout', 'spring_layout', 'random_layout', 'bipartite_layout', 'multipartite_layout',
    verbose : int, optional
        Print progress to screen. The default is 3.
        0: None, 1: Error, 2: Warning, 3: Info (default), 4: Debug, 5: Trace

    Returns
    -------
    dict containing pos and G
        pos : list.
            Positions of the nodes.
        G : Graph.
            Graph model
        node_properties: dict.
            Node properties.

    Examples
    --------

    """
    fig = None
    # Check whether edges are available
    if model['adjmat'].sum().sum()==0:
        if verbose>=3: print('[bnlearn]> Nothing to plot because no edges are present between nodes. ')
        return None

    # Plot properties
    defaults = {'height': '800px', 'width': '70%', 'notebook': False, 'layout': None, 'font_color': False, 'bgcolor': '#ffffff', 'directed': True, 'cdn_resources': 'remote', 'select_menu': True, 'filter_menu': True}
    params_interactive = {**defaults, **params_interactive}
    defaults = {'minscale': 1, 'maxscale': 10, 'figsize': (15, 10), 'height': None, 'width': None, 'font_size': 14, 'font_family': 'sans-serif', 'alpha': 0.8, 'layout': 'spring_layout', 'font_color': 'k', 'facecolor': '#ffffff', 'node_shape': 'o', 'edge_alpha': 0.8, 'arrowstyle': '-|>', 'arrowsize': 30, 'visible': True}
    params_static = {**defaults, **params_static}

    # DEPRECATED IN LATER VERSION
    if (params_static.get('width') is not None) or (params_static.get('height') is not None):
        # if verbose>=2: print('[bnlearn]> Warning: [height] and [width] will be removed in further version. Please use: params_static={"figsize": (15, 10)}.')
        params_static['figsize'] = (15 if params_static['width'] is None else params_static['width'], 10 if params_static['height'] is None else params_static['height'])
    # END BLOCK

    out = {}
    G = nx.DiGraph()  # Directed graph
    node_size_default = 10 if interactive else 800
    if (node_properties is not None) and (node_size is not None):
        if verbose>=2: print('[bnlearn]> Warning: if both "node_size" and "node_properties" are used, "node_size" will be used.')

    # Get node and edge properties if not user-defined
    if node_properties is None:
        node_properties = get_node_properties(model, node_size=node_size_default)
    if edge_properties is None:
        edge_properties = get_edge_properties(model, minscale=params_static['minscale'], maxscale=params_static['maxscale'])

    # Set default node size based on interactive True/False
    for key in node_properties.keys():
        if node_properties[key]['node_size'] is None:
            node_properties[key]['node_size']=node_size_default

    # Extract model if in dict
    if 'dict' in str(type(model)):
        bnmodel = model.get('model', None)
    else:
        bnmodel = model.copy()

    # get node properties
    nodelist, node_colors, node_sizes, edgelist, edge_colors, edge_weights = _plot_properties(G, node_properties, edge_properties, node_color, node_size)

    # Bayesian model
    if ('bayes' in str(type(bnmodel)).lower()) or ('pgmpy' in str(type(bnmodel)).lower()):
        if verbose>=3: print('[bnlearn] >Plot based on Bayesian model')
        # positions for all nodes
        G = nx.DiGraph(model['adjmat'])
        pos = network.graphlayout(G, pos=pos, scale=scale, layout=params_static['layout'], verbose=verbose)
    elif 'networkx' in str(type(bnmodel)):
        if verbose>=3: print('[bnlearn] >Plot based on networkx model')
        G = bnmodel
        pos = network.graphlayout(G, pos=pos, scale=scale, layout=params_static['layout'], verbose=verbose)
    else:
        if verbose>=3: print('[bnlearn] >Plot based on adjacency matrix')
        G = network.adjmat2graph(model['adjmat'])
        # Get positions
        pos = network.graphlayout(G, pos=pos, scale=scale, layout=params_static['layout'], verbose=verbose)

    # Plot
    if interactive:
        # Make interactive plot
        fig = _plot_interactive(model, params_interactive, nodelist, node_colors, node_sizes, edgelist, edge_colors, edge_weights, title, verbose=verbose)
    else:
        # Make static plot
        fig = _plot_static(model, params_static, nodelist, node_colors, node_sizes, G, pos, edge_colors, edge_weights, visible=params_static['visible'])

    # Store
    out['fig']=fig
    out['ax']=fig  # Should be removed in later releases
    out['pos']=pos
    out['G']=G
    out['node_properties']=node_properties
    out['edge_properties']=edge_properties
    return out




# %% Plot interactive
# def _plot_static(model, params_static, nodelist, node_colors, node_sizes, title, verbose=3):
def _plot_static(model, params_static, nodelist, node_colors, node_sizes, G, pos, edge_colors, edge_weights, visible=True):
    # Bootup figure
    fig = plt.figure(figsize=params_static['figsize'], facecolor=params_static['facecolor'])
    # nodes
    nx.draw_networkx_nodes(G, pos, nodelist=nodelist, node_size=node_sizes, alpha=params_static['alpha'], node_color=node_colors, node_shape=params_static['node_shape'])
    # edges
    # nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=30, edge_color=edge_color, width=edge_weights)
    nx.draw_networkx_edges(G, pos, arrowstyle=params_static['arrowstyle'], arrowsize=params_static['arrowsize'], edge_color=edge_colors, width=edge_weights, alpha=params_static['edge_alpha'])
    # Labels
    nx.draw_networkx_labels(G, pos, font_size=params_static['font_size'], font_family=params_static['font_family'], font_color=params_static['font_color'])
    # Plot text of the weights
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_color=params_static['font_color'])
    # Making figure nice
    # fig = plt.gca()
    # fig.set_axis_off()
    if visible:
        plt.show()
    # Return
    return fig



# %% Plot interactive
def _plot_interactive(model, params_interactive, nodelist, node_colors, node_sizes, edgelist, edge_colors, edge_weights, title, verbose=3):
    # If not notebook
    if not params_interactive['notebook']:
        # https://pyvis.readthedocs.io/en/latest/tutorial.html?highlight=cdn_resources#using-pyvis-within-jupyter-notebook
        params_interactive['cdn_resources']='local'

    # Try to import pyvis
    try:
        from pyvis.network import Network
        from IPython.core.display import display, HTML
    except ModuleNotFoundError:
        if verbose>=1: raise Exception('[bnlearn] >"pyvis" module is not installed. Please pip install first: "pip install pyvis"')
    # Convert adjacency matrix into Networkx Graph
    G = network.adjmat2graph(model['adjmat'])
    # Setup of the interactive network figure
    g = Network(**params_interactive)
    # Convert from graph G
    g.from_nx(G)
    # Nodes
    for i, _ in enumerate(g.nodes):
        g.nodes[i]['color']=node_colors[np.where(nodelist==g.nodes[i].get('label'))[0][0]]
        g.nodes[i]['size']=node_sizes[np.where(nodelist==g.nodes[i].get('label'))[0][0]]

    # Edges
    g_edges = list(map(lambda x: (x.get('from'), x.get('to')), g.edges))
    for i, _ in enumerate(g.edges):
        idx = np.where(list(map(lambda x: g_edges[i]==x, edgelist)))[0][0]
        g.edges[i]['color']=edge_colors[idx]
        g.edges[i]['weight']=edge_weights[idx]

    # Create advanced buttons
    g.show_buttons(filter_=['physics'])
    # Display
    filename = title.strip().replace(' ', '_') + '.html'
    g.show(filename, local=params_interactive['notebook'])
    display(HTML(filename))
    # webbrowser.open('bnlearn.html')
    return os.path.abspath(filename)


# %% Make DAG
def make_DAG(DAG, CPD=None, methodtype='bayes', checkmodel=True, verbose=3):
    """Create Directed Acyclic Graph based on list.

    Parameters
    ----------
    DAG : list
        list containing source and target in the form of [('A','B'), ('B','C')].
    CPD : list, array-like
        Containing TabularCPD for each node.
    methodtype : str (default: 'bayes')
        * 'bayes': Bayesian model
        * 'nb' or 'naivebayes': Special case of Bayesian Model where the only edges in the model are from the feature variables to the dependent variable. Or in other words, each tuple should start with the same variable name such as: edges = [('A', 'B'), ('A', 'C'), ('A', 'D')]
        * 'markov': Markov model
    checkmodel : bool
        Check the validity of the model. The default is True
    verbose : int, optional
        Print progress to screen. The default is 3.
        0: None, 1: ERROR, 2: WARN, 3: INFO (default), 4: DEBUG, 5: TRACE

    Returns
    -------
    dict keys:
        * 'adjmat': Adjacency matrix
        * 'model': pgmpy.models
        * 'methodtype': methodtype
        * 'model_edges': Edges

    Examples
    --------

    """
    if (CPD is not None) and (not isinstance(CPD, list)):
        CPD=[CPD]

    if methodtype=='nb': methodtype='naivebayes'

    if isinstance(DAG, dict):
        DAG = DAG.get('model', None)

    if (not isinstance(DAG, list)) and ('pgmpy' not in str(type(DAG))):
        raise Exception("[bnlearn] >Error: Input DAG should be a list. in the form [('A','B'), ('B','C')] or a <pgmpy.models.BayesianNetwork>")
    elif ('pgmpy' in str(type(DAG))):
        # Extract methodtype from existing model.
        if ('bayesianmodel' in str(type(DAG)).lower()):
            methodtype='bayes'
        elif('naivebayes' in str(type(DAG)).lower()):
            methodtype='naivebayes'
        if verbose>=3: print('[bnlearn] >No changes made to existing %s DAG.' %(methodtype))
    elif isinstance(DAG, list) and methodtype=='naivebayes':
        if verbose>=3: print('[bnlearn] >%s DAG created.' %(methodtype))
        edges=DAG
        DAG = NaiveBayes()
        DAG.add_edges_from(edges)
        # modeel.add_nodes_from(DAG)
    elif isinstance(DAG, list) and methodtype=='bayes':
        if verbose>=3: print('[bnlearn] >%s DAG created.' %(methodtype))
        DAG = BayesianNetwork(DAG)
    elif isinstance(DAG, list) and methodtype=='markov':
        from kolibri.backend.bn.MarkovNetwork import MarkovNetwork
        if verbose>=3: print('[bnlearn] >%s DAG created.' %(methodtype))
        DAG = MarkovNetwork(DAG)

    if CPD is not None:
        for cpd in CPD:
            DAG.add_cpds(cpd)
            if verbose>=3: print('[bnlearn] >Add CPD: %s' %(cpd.variable))
        # Check model
        if checkmodel:
            check_model(DAG, verbose=verbose)

    # Create adjacency matrix from DAG
    out = {}
    out['adjmat'] = dag2adjmat(DAG)
    out['model'] = DAG
    out['methodtype'] = methodtype
    out['model_edges'] = DAG.edges()
    return out



# %%  Convert adjacency matrix to vector
def vec2adjmat(source, target, weights=None, symmetric=True):
    """Convert source and target into adjacency matrix.

    Parameters
    ----------
    source : list
        The source node.
    target : list
        The target node.
    weights : list of int
        The Weights between the source-target values
    symmetric : bool, optional
        Make the adjacency matrix symmetric with the same number of rows as columns. The default is True.

    Returns
    -------
    pd.DataFrame
        adjacency matrix.

    Examples
    --------

    """
    if len(source)!=len(target): raise ValueError('[hnet] >Source and Target should have equal elements.')
    if weights is None: weights = [1] *len(source)

    df = pd.DataFrame(np.c_[source, target], columns=['source', 'target'])
    # Make adjacency matrix
    adjmat = pd.crosstab(df['source'], df['target'], values=weights, aggfunc='sum').fillna(0)
    # Get all unique nodes
    nodes = np.unique(list(adjmat.columns.values) +list(adjmat.index.values))
    # nodes = np.unique(np.c_[adjmat.columns.values, adjmat.index.values].flatten())

    # Make the adjacency matrix symmetric
    if symmetric:
        # Add missing columns
        node_columns = np.setdiff1d(nodes, adjmat.columns.values)
        for node in node_columns:
            adjmat[node]=0

        # Add missing rows
        node_rows = np.setdiff1d(nodes, adjmat.index.values)
        adjmat=adjmat.T
        for node in node_rows:
            adjmat[node]=0
        adjmat=adjmat.T

        # Sort to make ordering of columns and rows similar
        [IA, IB] = ismember(adjmat.columns.values, adjmat.index.values)
        adjmat = adjmat.iloc[IB, :]
        adjmat.index.name='source'
        adjmat.columns.name='target'

    return(adjmat)


# %% Convert DAG into adjacency matrix
def dag2adjmat(model, verbose=3):
    """Convert model into adjacency matrix.

    Parameters
    ----------
    model : object
        Model object.
    verbose : int, optional
        Print progress to screen. The default is 3.
        0: None, 1: ERROR, 2: WARN, 3: INFO (default), 4: DEBUG, 5: TRACE

    Returns
    -------
    pd.DataFrame
        adjacency matrix.

    Examples
    --------


    """
    adjmat = None
    if hasattr(model, 'nodes') and hasattr(model, 'edges'):
        adjmat = pd.DataFrame(data=False, index=model.nodes(), columns=model.nodes()).astype('bool')
        # Fill adjmat with edges
        edges = model.edges()
        # Run over the edges
        for edge in edges:
            adjmat.loc[edge[0], edge[1]]=True
        adjmat.index.name='source'
        adjmat.columns.name='target'
    else:
        if verbose>=1: print('[bnlearn] >Could not convert to adjmat because nodes and/or edges were missing.')
    return(adjmat)


# %% Check model CPDs
def check_model(DAG, verbose=3):
    """Check if the CPDs associated with the nodes are consistent.

    Parameters
    ----------
    DAG : Object.
        Object containing CPDs.
    verbose : int, optional
        Print progress to screen. The default is 3.
        0: None, 1: ERROR, 2: WARN, 3: INFO (default), 4: DEBUG, 5: TRACE

    Returns
    -------
    None.

    """
    if verbose>=3: print('[bnlearn] >Check whether CPDs sum up to one.')
    if isinstance(DAG, dict): DAG = DAG.get('model', None)
    if DAG is not None:
        for cpd in DAG.get_cpds():
            if not np.all(cpd.values.astype(Decimal).sum(axis=0)==1):
                if verbose>=3: print('[bnlearn] >CPD [%s] does not add up to 1 but is: %s' %(cpd.variable, cpd.values.sum(axis=0)))
        if verbose>=3: print('[bnlearn] >Check whether CPDs associated with the nodes are consistent: %s' %(DAG.check_model()))
    else:
        if verbose>=2: print('[bnlearn] >No model found containing CPDs.')
def query2df(query, variables=None, verbose=3):
    """Convert query from inference model to a dataframe.

    Parameters
    ----------
    query : Object from the inference model.
        Convert query object to a dataframe.
    variables : list
        Order or select variables.

    Returns
    -------
    df : pd.DataFrame()
        Dataframe with inferences.

    """
    states = []
    getP = []
    for value_index, prob in enumerate(itertools.product(*[range(card) for card in query.cardinality])):
        states.append(prob)
        getP.append(query.values.ravel()[value_index])

    df = pd.DataFrame(data=states, columns=query.scope())
    df['p'] = getP
    # Order or filter on input variables
    if variables is not None:
        # Add Pvalue column
        variables = variables + ['p']
        df = df[variables]

    # Print table to screen
    if verbose>=3:
        print('[bnlearn] >Data is stored in [query.df]')
        print(tabulate(df, tablefmt="grid", headers="keys"))

    return df
def print_CPD(DAG, checkmodel=False, verbose=3):
    """Print DAG-model to screen.

    Parameters
    ----------
    DAG : pgmpy.models.BayesianNetwork
        model of the DAG.
    checkmodel : bool
        Check the validity of the model. The default is True

    Returns
    -------
    dict
        Dictionary containing the CPDs.

    Examples
    --------

    """
    # config = None
    CPDs = {}
    if isinstance(DAG, dict):
        DAG = DAG.get('model', None)

    # Print CPDs
    # if config['method']=='ml' or config['method']=='maximumlikelihood':
    try:
        if ('markovnetwork' in str(type(DAG)).lower()):
            if verbose>=3: print('[bnlearn] >Converting markovnetwork to Bayesian model')
            DAG=DAG.to_bayesian_model()

        if 'MaximumLikelihood' in str(type(DAG)):
            # print CPDs using Maximum Likelihood Estimators
            for node in DAG.state_names:
                print(DAG.estimate_cpd(node))
        elif ('bayesiannetwork' in str(type(DAG)).lower()) or ('naivebayes' in str(type(DAG)).lower()):
            # print CPDs using Bayesian Parameter Estimation
            if len(DAG.get_cpds())==0:
                raise Exception('[bnlearn] >Error! This is a Bayesian DAG containing only edges, and no CPDs. Tip: you need to specify or learn the CPDs. Try: DAG=bn.parameter_learning.fit(DAG, df). At this point you can make a plot with: bn.plot(DAG).')
                return
            for cpd in DAG.get_cpds():
                CPDs[cpd.variable] = query2df(cpd, verbose=verbose)
                if verbose>=3:
                    print("CPD of {variable}:".format(variable=cpd.variable))
                    print(cpd)
            if ('bayesiannetwork' in str(type(DAG)).lower()):
                if verbose>=3: print('[bnlearn] >Independencies:\n%s' %(DAG.get_independencies()))

            if verbose>=3:
                print('[bnlearn] >Nodes: %s' %(DAG.nodes()))
                print('[bnlearn] >Edges: %s' %(DAG.edges()))

        if checkmodel:
            check_model(DAG, verbose=3)
    except:
        if verbose>=2: print('[bnlearn] >No CPDs to print. Hint: Add CPDs as following: <bn.make_DAG(DAG, CPD=[cpd_A, cpd_B, etc])> and use bnlearn.plot(DAG) to make a plot.')

    # Returning dict with CPDs
    return CPDs

# %% Compute structure scores.
def structure_scores(model, df, scoring_method=['k2', 'bds', 'bic', 'bdeu'], verbose=3, **kwargs):
    """Compute structure scores.

    Description
    -----------
    Each model can be scored based on its structure. However, the score doesn't have very straight forward
    interpretebility but can be used to compare different models. A higher score represents a better fit.
    This method only needs the model structure to compute the score. The structure score functionality
    can be found here: :func:`bnlearn.bnlearn.structure_scores`.

    Parameters
    ----------
    model: The bnlearn instance such as pgmpy.base.DAG or pgmpy.models.BayesianNetwork
        The model whose score needs to be computed.

    df: pd.DataFrame instance
        The dataset against which to score the model.

    scoring_method: str ( k2 | bdeu | bds | bic )
        The following four scoring methods are supported currently: 1) K2Score
        2) BDeuScore 3) BDsScore 4) BicScore

    kwargs: kwargs
        Any additional parameters parameters that needs to be passed to the
        scoring method.

    Returns
    -------
    Model score: float
        A score value for the model.

    Examples
    --------
    """
    method = None
    show_message = True
    scores = {}
    # Get models and method
    if isinstance(model, dict):
        method = model.get('config')['method']
        model = model.get('model', None)
    if isinstance(scoring_method, str): scoring_method = [scoring_method]
    if verbose>=3: print('[bnlearn] >Compute structure scores %s for model comparison (higher is better).' %(scoring_method))

    # Return if method not supported
    if np.any(np.isin(method, ['cs', 'constraintsearch'])):
        if verbose>=2: print('[bnlearn] >Warning: Structure scoring could not be computed. Method [%s] not supported.' %(method))
        return scores

    # Compute structure scores
    if model is not None:
        for s in scoring_method:
            try:
                scores[s] = structure_score(model, df, scoring_method=s)
            except:
                if verbose>=2 and show_message:
                    print('[bnlearn] >Warning: Structure scoring could not be computed. DataFrame issues (?)')
                    show_message=False
    # Return
    return scores


def _filter_df(adjmat, df, verbose=3):
    """Adjacency matrix and dataframe columns are checked for consistency."""
    remcols = df.columns[~np.isin(df.columns.values, adjmat.columns.values)].values
    if len(remcols)>0:
        if verbose>=3: print('[bnlearn] >Removing columns from dataframe to make consistent with DAG [%s]' %(remcols))
        df.drop(labels=remcols, axis=1, inplace=True)
    return df


# %%  Convert adjacency matrix to vector
def adjmat2vec(adjmat, min_weight=1):
    """Convert adjacency matrix into vector with source and target.

    Parameters
    ----------
    adjmat : pd.DataFrame()
        Adjacency matrix.

    min_weight : float
        edges are returned with a minimum weight.

    Returns
    -------
    pd.DataFrame()
        nodes that are connected based on source and target

    Examples
    --------

    """
    # Convert adjacency matrix into vector
    adjmat = adjmat.stack().reset_index()
    # Set columns
    adjmat.columns = ['source', 'target', 'weight']
    # Remove self loops and no-connected edges
    Iloc1 = adjmat['source']!=adjmat['target']
    Iloc2 = adjmat['weight']>=min_weight
    Iloc = Iloc1 & Iloc2
    # Take only connected nodes
    adjmat = adjmat.loc[Iloc, :]
    adjmat.reset_index(drop=True, inplace=True)
    return(adjmat)

def to_bayesiannetwork(model, verbose=3):
    """Convert adjacency matrix to BayesianNetwork.

    Description
    -----------
    Convert a adjacency to a Bayesian model. This is required as some of the
    functionalities, such as ``structure_learning`` output a DAGmodel.
    If the output of ``structure_learning`` is provided, the adjmat is extracted and processed.

    Parameters
    ----------
    model : pd.DataFrame()
        Adjacency matrix.

    Raises
    ------
    Exception
        The input should not be None and if a model (as dict) is provided, the key 'adjmat' should be included.

    Returns
    -------
    BayesianNetwork : Object
        BayesianNetwork that can be used in ``parameter_learning.fit``.

    """
    if isinstance(model, dict):
        adjmat = model.get('adjmat', None)
    else:
        adjmat = model
    if adjmat is None: raise Exception('[bnlearn] >Error: input for "bayesiannetwork" should be adjmat or a dict containing a key "adjmat".')

    if verbose>=3: print('[bnlearn] >Converting adjmat to BayesianNetwork.')

    # Convert to vector
    vec = adjmat2vec(adjmat)[['source', 'target']].values.tolist()
    # Make BayesianNetwork
    bayesianmodel = BayesianNetwork(vec)
    # Return
    return bayesianmodel
