import networkx as nx
from pgmpy.base import DAG

# ====================================== extract ======================================

# TODO: a plot function for all nodes in route x->y, with moderators
# DONE: need a function to plot moderator properly. Question asked at https://github.com/networkx/networkx/discussions/5997


def buildGraph(edges, moderatorDict=None):
    G = DAG(edges)
    if moderatorDict is not None:
        G.add_nodes_from(moderatorDict.values())
    return G


def findAllEdges(df_path, df_def, df_ref, paper_id, delimiter="-"):
    """
    use paper name to locate all nodes defined with such reference entry.
    filter path map with all selected nodes to find all relevant edges, including moderators' edges
    which should be an paper id
    """
    paper = df_ref["Reference"][paper_id]  # select paper
    nodesIdx = df_def.index[df_def["Reference"] == paper].tolist()  # select nodes rows
    nodeIds = df_def["ID"][nodesIdx].tolist()  # get real node id
    nodeNames = df_def["Node"][nodesIdx].tolist()  # get node names
    nodeMap = dict(zip(nodeIds, nodeNames))

    edges = []
    moderatorDict = {}
    numMod = 0

    for i in nodeIds:
        found = df_path.index[df_path["ID.1"] == i].tolist()
        starts = df_path["ID.1"][found].tolist()
        ends = df_path["ID"][found].tolist()
        for st, ed in zip(starts, ends):
            ed = ed.replace(delimiter, "->")
            if "->" in ed:
                numMod += 1
                moderatorDict[ed] = st  # same edge referenced by multiple moderators?
            else:
                edges.append((st, ed))
    return edges, moderatorDict, nodeMap


"""
when generate final route, for each nodes on the route, moderator check is needed.
moderator status is associated with edge according to 08/20 discussion
for instance: B --> D, moderator M -> BD. it can be transformed into B --> (M) --> D.
When edge BD is selected, check hasModerator(BD), if True, then B -> B(M)
"""
# moderatorDict = {'B->D': 'M0'}
def hasModerator(edge, mdict):
    if edge in mdict:
        return mdict[edge]
    return ""


def dfs(G, root, depth):
    """
    find all routes at certain depth from given root, using dfs.
    """
    visitedList = []
    # recursion helper
    def _dfs(G, root, depth, visited):
        # print(visitedList, root, visited, depth) # debug
        visited.append(root)
        if depth == 0:
            visitedList.append(visited)
            # print(visitedList, root, visited, depth) # debug
        for pa in G.get_parents(root):
            _dfs(G, pa, depth - 1, visited.copy())

    _dfs(G, root, depth, [])
    return visitedList


def dfs2(G, x, y):
    """
    find all routes between given x and y, using dfs.
    we know the direction must be x-->...-->y given our assumption of x and y
    use depth first search to find all the path btw x and y
    """
    visitedList = []

    def _dfs2(G, x, y, visited):
        visited.append(x)
        # print(visited)
        if x == y:
            visitedList.append(visited)
        for cc in G.get_children(x):
            _dfs2(G, cc, y, visited.copy())

    _dfs2(G, x, y, [])
    return visitedList


def dfs3(G, root, depth, mdict):
    """
    find all nodes reachable at certain depth, together with all moderators along the way, from given root, using dfs.
    """
    # findRoutes can do the same task, but return the complete routes.
    visitedList = []

    def _dfs3(G, root, depth, mdict, prev, mediVisited):
        # print(prev, root, mediVisited)
        edge = f"{root}->{prev}"
        # print(edge)
        md = hasModerator(edge, mdict)
        if md != "":
            # print(edge, md)
            mediVisited.append(md)
        if depth == 0:
            select = [root] + mediVisited
            visitedList.append(select)
        for pa in G.get_parents(root):
            _dfs3(G, pa, depth - 1, mdict, root, mediVisited.copy())

    _dfs3(G, root, depth, mdict, root, [])
    return visitedList


def findRoutesAt(G, y, depth, mdict):
    """
    find all routes at certain depth, together with all moderators along the way, from given root, using dfs.
    using `dfs()`
    """
    # dfs3 can do the same task, but only return the reachable nodes, instead of the full route.
    routes = dfs(G, y, depth)
    if depth == 0 or len(routes) == 0:  # depth == 0 or beyond reachable depth
        return routes
    for rr in routes:
        for i in range(1, len(rr)):
            edge = f"{rr[i]}->{rr[i-1]}"
            # print(edge)
            md = hasModerator(edge, mdict)
            if md != "":
                rr[i] += f"({md})"
    return routes


def findRoutesUpTo(G, y, depth, mdict, start=1):
    """
    find all routes at certain depth, up to given `depth`
    """
    rdict = {}
    for d in range(start, depth + 1):
        droute = findRoutesAt(G, y, d, mdict)
        rdict[d] = len(droute), droute
    return rdict


def findNodesUpTo(G, y, depth, mdict, start=1):
    """
    find all nodes reachable at certain depth, up to given `depth`
    """
    rdict = {}
    for d in range(start, depth + 1):
        droute = dfs3(G, y, d, mdict)
        rdict[d] = len(droute), droute
    return rdict


def findDSepZ(G, x, y):
    """
    find z s.t. (z _|_ y | x)

    d_separated(x,y,z): test if (x _|_ y | z) is true
    we have given y, found couple of x, we want to find z
    so we should be testing z, s.t. (z _|_ y | x), `nx.d_separated(z, y, x)`, with various z
    since x --> .. --> y, anything on the path x --> y cannot be z
    z can only be found as x's descendant?
    """

    # DONE: z can't be disconnected     node, also, z and m can't be the same
    allRoutes = dfs2(G, x, y)
    nodesOnRoutes = set(n for route in allRoutes for n in route)
    nodesRest = (
        set(G.nodes) - nodesOnRoutes - set(G.get_parents(y)) - set(G.get_children(y))
    )
    # print(nodesRest)
    """
    Q: do we expect z's instantiation to be freely assignable?
    Q: whether request z to be ancestors of x?
    Q: can z be children of x?   
    """
    zCandidates = []
    for z in nodesRest:
        isGood = nx.has_path(
            G.to_undirected(as_view=True), z, x
        )  # in our case, z must be connected to the clique
        isGood &= nx.d_separated(G, set([z]), set([y]), set([x]))
        if isGood:
            zCandidates.append(z)

        # print(f'{z} _|_ {y} | {x}? {isGood}')
    return zCandidates


def findAllZ(G, xmAll, y):
    """
    find all possible z given x and y
    fix: z is only possible when it's "connected" to the target clip
    Q: maybe we should also remove moderators from possible Z?
    return dict of format {(xmAll): z}
    """
    zAll = []

    for xm in xmAll:
        # x = xm[-1]
        x = xm[0]
        if len(xm) > 1:
            """
            maybe we should remove moderator from possible Z?
            Yes, we should, and it's taken care of since G doesn't have node2edge connection
            """
            pass
        z = findDSepZ(G, x, y)  # moderatorDict as 4th argument
        zAll.append(z)  # could be empty set

        # print(x, y, z)
    return zAll


# ==================================== generation ====================================


def findAllType1(G, mdict):
    """
    find all (y, (xm)) pairs, up to depth 5
    """
    type1 = set()
    for y in G.nodes():
        xmAllDepth = findNodesUpTo(G, y, 5, mdict)
        for cnt, xms in xmAllDepth.values():
            if cnt != 0:
                for xm in xms:
                    type1.add((y, tuple(xm)))
            else:
                break  # deeper depth depends on shallow result.
    return type1


def findAllType2(G, mdict):
    """
    find all (y, (xm), (zs)) pairs, up to depth 5
    """
    type2 = set()
    for y in G.nodes():
        xmAllDepth = findNodesUpTo(G, y, 5, mdict)
        for cnt, xms in xmAllDepth.values():
            if cnt != 0:
                zAll = findAllZ(G, xms, y)
                for xm, zs in zip(xms, zAll):
                    if len(zs) != 0:
                        type2.add((y, tuple(xm), tuple(zs)))
            else:
                break  # deeper depth depends on shallow result.
    return type2


def findAllType3A(G, mdict):
    """
    find all (y, (xm)) pairs, up to depth 5, must have moderators
    """
    type3 = set()
    if len(mdict) != 0:
        type1 = findAllType1(G, mdict)
        type3 = set((y, xm) for y, xm in type1 if len(xm) > 1)
    return type3
