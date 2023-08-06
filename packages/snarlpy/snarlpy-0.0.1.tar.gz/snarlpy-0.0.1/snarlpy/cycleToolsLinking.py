# @Author:  Felix Kramer
# @Date:   2021-04-23T12:48:28+02:00
# @Email:  kramer@mpi-cbg.de
# @Project: go-with-the-flow
# @Last modified by:   felix
# @Last modified time: 2022-07-28T18:43:49+02:00
# @License: MIT
import numpy as np
from dataclasses import dataclass, field
from scipy.integrate import nquad
import itertools as itl
from scipy import interpolate
import snarlpy.simpleCycles as simpleCycles


@dataclass
class linkedCycles_tools(simpleCycles.simple_cycles):

    """
    A class f function tools to compte linking of cycle basis of simple,
    spatially embedded graphs.
    Attributes:
        tck (dict):\n
            Spline parameters for curve smoothening
        edge_res (int):\n
            Edge point resolution.
        XS (list):\n
            Array of curve parameters (0,1) for edge point densification.
        N (int):\n
            ???
        res (int):\n
            Numeric resoltuion of Gauss map (double integral) evaluation.
        threshold (float):\n
            Linkage number demanded accuracy.
        x (list):\n
            An array holding curve parameters for smoothened curves.
        dxy (float):\n
            Double integral infinitesimal square factor.

    Methods:
        __post_init__()
            The model post_init function.
        calc_linkage_cycleSets_nxGraph(cycle_sets1, cycle_sets2)
            Compute the linkage dictionaries in boolean and numeric form for
            two sets of cycle bases (in networkx format).
        extract_points_nxGraph(cycle_sets1, cycle_sets2)
            Extract the polygonial representation of each edge of the given
            graph sets.
        calc_linkage_cycleSets_points3D(curves_set1, curves_set2)
            Compute the linkage dictionaries in boolean and numeric form for
            two sets of cycle bases (in polygonial format).
        calc_linkage_points3D(curves_set1, curves_set2)
            Compute the linkage of polygonial curves in 3D via the Gauss map
            for each cycle pairing.
        get_geoInfo(curve_sets)
            Compute cycle centers and maximal point distance from center (For
            pre-sorting spatially distant cycles which cant'possibly be linked)
        compute_link_number(curve1, curve2):
            Compute the specific link for a pair of curves, via Gauss map
            evaluation.
        get_smooth_curve(points3D)
            Smoothing of polygonial curves in order to improve results for
            sharp bending points and fourther function generator dependencies.
        refine_curve_points(points3D)
            Increase point density of the graph'sedges, by inserting extra
            points along the line segments.
        get_smooth_points(t, tck)
            Create a smooth 3D point representation by utilizing previoulsy
            calucalted spline parameters and current curve parameters.
        get_smooth_director(t, tck):
            Create a smooth 3D point representation of the curves tangent by
            utilizing previoulsy calucalted spline parameters and current curve
            parameters.
        gauss_map(points, tangents)
            Gauss map evaluation utilizing the entirety of curve points and
            their tangents (equal to entire double integral kernel evaluation).

    """
    kwargs = dict(init=False, repr=False)

    tck: dict = field(default_factory=dict, **kwargs)
    edge_res: int = field(default=5, **kwargs)
    XS: list = field(default_factory=list, **kwargs)
    # N: int = field(default=3, **kwargs)
    res: int = field(default=200, **kwargs)
    threshold: float = field(default=0.05, **kwargs)

    x: list = field(default_factory=list, **kwargs)
    dxy: float = field(default=0., **kwargs)

    def __post_init__(self):
        # def __init__(self):
        # super(linkedCycles_tools, self).__init__()
        # self.tck = {}
        # self.edge_res = 5
        self.XS = np.linspace(0, 0.95, self.edge_res)
        # self.N = 3
        # self.res = 200
        # self.threshold = 0.05
        # self.limit = 50

        self.x = np.linspace(0, 1, self.res)
        self.dxy = (self.x[1] - self.x[0])**2

    def calc_linkage_cycleSets_nxGraph(self, cycle_sets1, cycle_sets2):
        """
        Compute the linkage dictionaries in boolean and numeric form for two
        sets of cycle bases (in networkx format).

        Args:
            cycle_sets1 (list): \n
                A list of networkx.Graph objects representing the cycle basis
                of graph #1.
            cycle_sets2 (list): \n
                A list of networkx.Graph objects representing the cycle basis
                of graph #2.
        Returns:
            dict: \n
                A dictionary containing the boolean value of linkage for each
                cycle pair of the input bases.
            dict: \n
                A dictionary containing the numeric value of linkage (Gauss
                map) for each cycle pair of the input bases.
        """

        # precalc curve points and tangents for a given set of curves
        cs = self.extract_points_nxGraph(cycle_sets1, cycle_sets2)
        bool_res, res = self.calc_linkage_cycleSets_points3D(cs[0], cs[1])

        return bool_res, res

    def extract_points_nxGraph(self, cycle_sets1, cycle_sets2):
        """
        Extract the polygonial representation of each edge of the given graph
        sets.

        Args:
            cycle_sets1 (list): \n
                A list of networkx.Graph objects representing the cycle basis
                of graph #1.
            cycle_sets2 (list): \n
                A list of networkx.Graph objects representing the cycle basis
                of graph #2.
        Returns:
            list: \n
                A list of polygons for each input basis representing the
                spatially embeded curve for each basis cycle.

        """
        curves_sets = []
        for i, cs in enumerate([cycle_sets1, cycle_sets2]):

            curves_points = []
            for c in cs:
                cycle_points = self.extract_path_origin(c)
                curves_points.append(cycle_points)

            curves_sets.append(curves_points)

        return curves_sets

    def calc_linkage_cycleSets_points3D(self, curves_set1, curves_set2):
        """
        Compute the linkage dictionaries in boolean and numeric form for two
        sets of cycle bases (in polygonial format).

        Args:
            cycle_sets1 (list): \n
                A list of 3D-point sets representing the cycle basis
                of graph #1.
            cycle_sets2 (list): \n
                A list of 3D-point sets representing the cycle basis
                of graph #2.
        Returns:
            dict: \n
                A dictionary containing the boolean value of linkage for each
                cycle pair of the input bases.
            dict: \n
                A dictionary containing the numeric value of linkage (Gauss
                map) for each cycle pair of the input bases.
        """
        # precalc curve points and tangents for a given set of curves
        res = self.calc_linkage_points3D(curves_set1, curves_set2)
        bool_res = {}

        for kc, vc in res.items():

            if np.round(vc, 0) == 0:
                bool_res[kc] = False
            else:
                bool_res[kc] = True

        return bool_res, res

    def calc_linkage_points3D(self, curves_set1, curves_set2):
        """
        Compute the linkage of polygonial curves in 3D via the Gauss map for
        each cycle pairing.

        Args:
            cycle_sets1 (list): \n
                A list of 3D-point sets representing the cycle basis
                of graph #1.
            cycle_sets2 (list): \n
                A list of 3D-point sets representing the cycle basis
                of graph #2.
        Returns:
            dict: \n
                A dictionary containing the numeric value of linkage (Gauss
                map) for each cycle pair of the input bases.

        """
        res = {}
        curves_sets = [curves_set1, curves_set2]

        # pre-sort non-overlapping cycles
        k = [len(c) for c in curves_sets]
        all_idx = itl.product(range(k[0]), range(k[1]))
        center, dist_fromCenter = self.get_geoInfo(curves_sets)

        check_list = []
        for i, j in all_idx:

            res[(i, j)] = 0.

            dc = np.subtract(center[0][i], center[1][j])
            ds = dist_fromCenter[0][i] + dist_fromCenter[1][j]
            dist_c = np.linalg.norm(dc)
            dist = dist_c-ds

            if dist < 0:
                check_list.append((i, j))

        # compute linking numbers only for spatially overlapping curves
        curve_pairs = [[curves_set1[i], curves_set2[j]] for i, j in check_list]
        # linkage_pairs = itl.starmap(self.compute_link_number, curve_pairs)

        # parallel computing of loop combinations neccessary?
        import multiprocessing as mp
        pool = mp.Pool(processes=4)
        linkage_pairs = pool.starmap(self.compute_link_number, curve_pairs)
        pool.close()
        #
        for i, lk in enumerate(linkage_pairs):
            res.update({check_list[i]: lk})

        return res

    def get_geoInfo(self, curve_sets):

        """
        Compute cycle centers and maximal point distance from center (For
        pre-sorting spatially distant cycles which cant'possibly be linked)

        Args:
            curve_sets (list): \n
                A list of polygons for each input basis representing the
                spatially embeded curve for each basis cycle.

        Returns:
            dict: \n
                A dictionary containing cycle centers for each cycle basis
                (3D points)
            dict: \n
                A dictionary containing maximal point distance from the center
                for each cycle basis.

        """
        center = {0: [], 1: []}
        dist_fromCenter = {0: [], 1: []}

        for i, curves in enumerate(curve_sets):
            for j, cs in enumerate(curves):

                center[i].append(np.mean(cs, axis=0))

                ds = np.subtract(center[i][-1], cs)
                max_ds = np.amax(np.linalg.norm(ds, axis=1))
                dist_fromCenter[i].append(max_ds)

        return center, dist_fromCenter

    def compute_link_number(self, curve1, curve2):
        """
        Compute the specific link for a pair of curves, via Gauss map
        evaluation.

        Args:
            curve_1 (list): \n
                A list 3D points (ordered) forming a closed curve (cycle #1).
            curve_1 (list): \n
                A list 3D points (ordered) forming a closed curve (cycle #2).

        Returns:
            float: \n
                Non-rounded result of numeric double integral evaluation.

        """
        # init path integrals parameters
        xSet = self.x
        dxy = self.dxy
        steps = self.res

        refining = True
        while refining:

            # generate smooth curves for each cycle
            points, tangents = [], []
            for i, curve in enumerate([curve1, curve2]):

                tck = self.get_smooth_curve(curve)
                p = [self.get_smooth_points(xs, tck) for xs in xSet]
                t = [self.get_smooth_director(xs, tck) for xs in xSet]

                points.append(p)
                tangents.append(t)

            lk = self.gauss_map(points, tangents)*dxy/(4.*np.pi)

            # check accuracy, refine path integrals if neccessary
            dl = np.absolute(np.round(lk, 0)-lk)
            if dl < self.threshold:
                refining = False
                break
            else:
                steps *= 2
                xSet = np.linspace(0, 1, steps)
                dx = xSet[1]-xSet[0]
                dxy = dx**2

                if steps > 2000:
                    print('slow convergence, error: ')
                    print(dl)
                    print('refining path integral: ')
                    print(steps)

        return lk

    def get_smooth_curve(self, points3D):
        """
        Smoothing of polygonial curves in order to improve results for sharp
        bending points and fourther function generator dependencies.

        Args:
            points3D (list): \n
                A list 3D points (ordered) forming a closed curve.

        Returns:
            tuple: \n
                (t,c,k) a tuple containing the vector of knots, the B-spline
                coefficients, and the degree of the spline.

        """
        # generate more comprehensive point sets from line curves

        curve_points = self.refine_curve_points(points3D)
        f = np.array(curve_points)

        x = f[:, 0]
        y = f[:, 1]
        z = f[:, 2]

        x[-1] = x[0]
        y[-1] = y[0]
        z[-1] = z[0]

        # smooth curves
        tck, u = interpolate.splprep([x, y, z], s=0., per=1)

        return tck

    def refine_curve_points(self, points3D):
        """
        Increase point density of the graph'sedges, by inserting extra points
        along the line segments.

        Args:
            points3D (list): \n
                A list 3D points (ordered) forming a closed curve, each
                consecutive tuple represents an edge from the graph.

        Returns:
            list: \n
                Denser 3D point representation of closed curves.

        """
        new_curve_points = []
        for i, p1 in enumerate(points3D):

            p2 = points3D[(i+1) % len(points3D)]
            dp = np.subtract(p2, p1)

            new_set = [np.add(x*dp, p1) for x in self.XS]
            new_curve_points += new_set

        return new_curve_points

    def get_smooth_points(self, t, tck):
        """
        Create a smooth 3D point representation by utilizing previoulsy
        calucalted spline parameters and current curve parameters.

        Args:
            t (list): \n
                Current curve parameter.
            tck (tuple): \n
                (t,c,k) a tuple containing the vector of knots, the B-spline
                coefficients, and the degree of the spline.

        Returns:
            ndarrray: \n
                A 3D point as part of the smooth curve representation.

        """
        x, y, z = interpolate.splev(t, tck)

        return np.array((x, y, z))

    def get_smooth_director(self, t, tck):
        """
        Create a smooth 3D point representation of the curves tangent by
        utilizing previoulsy calucalted spline parameters and current curve
        parameters.

        Args:
            t (list): \n
                Current curve parameter.
            tck (tuple): \n
                (t,c,k) a tuple containing the vector of knots, the B-spline
                coefficients, and the degree of the spline.

        Returns:
            ndarrray: \n
                A 3D point as part of the smooth curve representation.

        """
        dt = 0.00001
        p_f = np.array(self.get_smooth_points(t+dt, tck))
        p_b = np.array(self.get_smooth_points(t-dt, tck))

        d = np.subtract(p_f, p_b)/(2. * dt)

        return d

    def gauss_map(self, points, tangents):
        """
        Gauss map evaluation utilizing the entirety of curve points and their
        tangents (equal to entire double integral kernel evaluation).

        Args:
            points (list): \n
                A list of 3D points as part of the smooth curve representation,
                for each cyce.
            tangents (tuple): \n
                A list 3D points as part of the smooth curve representation,
                for each cycle.

        Returns:
            float: \n
                The evaluated, non-rounded value of the Gauss map kernel.

        """
        gm = 0.
        d1 = tangents[0]
        d2 = tangents[1]

        for i, r1 in enumerate(points[0]):

            df = np.subtract(r1, points[1])
            df12 = np.divide(df.transpose(), np.linalg.norm(df, axis=1)**3)
            d12 = np.cross(d1[i], d2)
            gm += np.einsum('ij,ij', d12, df12.transpose())

        return gm


@dataclass
class linkedCycles_extraTools(linkedCycles_tools):
    """
    A class f function tools to compte linking of cycle basis of simple,
    spatially embedded graphs.
    Attributes:
        tck (dict):\n
            Spline parameters for curve smoothening
        edge_res (int):\n
            Edge point resolution.
        XS (list):\n
            Array of curve parameters (0,1) for edge point densification.
        N (int):\n
            ???
        res (int):\n
            Numeric resoltuion of Gauss map (double integral) evaluation.
        threshold (float):\n
            Linkage number demanded accuracy.
        limit (int):\n
            Internal limit numbers.
        lm (list):\n
            List of internal limit numbers.
        itvl (list):\n
            Double integral borders.
        x (list):\n
            An array holding curve parameters for smoothened curves.
        dxy (float):\n
            Double integral infinitesimal square factor.

    Methods:
        __post_init__()
            The model post_init function.
        calc_linkage_cycleSets_nxGraph(cycle_sets1, cycle_sets2)
            Compute the linkage dictionaries in boolean and numeric form for
            two sets of cycle bases (in networkx format).
        extract_points_nxGraph(cycle_sets1, cycle_sets2)
            Extract the polygonial representation of each edge of the given
            graph sets.
        calc_linkage_cycleSets_points3D(curves_set1, curves_set2)
            Compute the linkage dictionaries in boolean and numeric form for
            two sets of cycle bases (in polygonial format).
        calc_linkage_points3D(curves_set1, curves_set2)
            Compute the linkage of polygonial curves in 3D via the Gauss map
            for each cycle pairing.
        get_geoInfo(curve_sets)
            Compute cycle centers and maximal point distance from center (For
            pre-sorting spatially distant cycles which cant'possibly be linked)
        compute_link_number(curve1, curve2):
            Compute the specific link for a pair of curves, via Gauss map
            evaluation.
        get_smooth_curve(points3D)
            Smoothing of polygonial curves in order to improve results for
            sharp bending points and fourther function generator dependencies.
        refine_curve_points(points3D)
            Increase point density of the graph'sedges, by inserting extra
            points along the line segments.
        get_smooth_points(t, tck)
            Create a smooth 3D point representation by utilizing previoulsy
            calucalted spline parameters and current curve parameters.
        get_smooth_director(t, tck):
            Create a smooth 3D point representation of the curves tangent by
            utilizing previoulsy calucalted spline parameters and current curve
            parameters.
        gauss_map(points, tangents)
            Gauss map evaluation utilizing the entirety of curve points and
            their tangents (equal to entire double integral kernel evaluation).
        compute_link_number(curve1, curve2)
            Compute the linking number of two closed curves
            (3D point representation).

    """
    # def __init__(self):
    #
    #     super(linkedCycles_extraTools, self).__init__()
    kwargs = dict(init=False, repr=False)
    limit: int = field(default=50, **kwargs)
    lm: list = field(default_factory=list, **kwargs)
    itvl: list = field(default_factory=list, **kwargs)

    def __post_init__(self):

        self.lm = [dict(limit=self.limit) for i in range(2)]
        self.itvl = [(0, 1), (0, 1)]

    def compute_link_number(self, curve1, curve2):

        """
        Compute the linking number of two closed curves
        (3D point representation).

        Args:
            curve_1 (list): \n
                A list of 3D-point sets representing a cycle
                of graph #1.
            curve_2 (list): \n
                A list of 3D-point sets representing a cycle
                of graph #2.
        Returns:
            dict: \n
                A dictionary containing the numeric value of the linking number
                integral (Gauss map).

        """
        # decompose any polygon train as a series of straigh line functions
        T = []
        for curve in [curve1, curve2]:

            cs = curve+[curve[0]]
            tangents = [
                np.subtract(cs[i+1], ps) for i, ps in enumerate(cs[:-1])
                ]
            T.append(tangents)

        p = itl.product(curve1, curve2)
        t = itl.product(*T)
        pars = zip(p, t)

        # calculate the linking number as evaluation of all line segments
        # combined
        lk = 0.
        for p, t in pars:

            t1, t2 = t
            t12 = np.cross(*t)
            p12 = p[0]-p[1]

            lk += nquad(
                    self.gauss_map,
                    ranges=self.itvl,
                    args=(p12, t, t12),
                    opts=self.lm
                )[0]

        res = lk/(4.*np.pi)

        return res

    def gauss_map(self, x1, x2, p12, t, t12):

        """
        Gauss mappiecewise linear bits of the entire closed super-curves.

        Args:
            x1 (float):
                Curve parameter #1.
            x2 (float):
                Curve parameter #2.
            p12 (ndarray):
                Anchor point difference.
            t (list):
                A list of ndarrays representing the current edge tangent
                vector.
            p12 (ndarray):
                Anchor point difference.

        Returns:
            float: \n
                The evaluated, non-rounded value of the Gauss map kernel bit.
        """
        # df = p12+x1*t[0]-x2*t[1]
        # df12 = df/((df[0]**2+df[1]**2+df[2]**2)**1.5)
        # gm = df12[0] * t12[0] + df12[1] * t12[1] + df12[2] * t12[2]

        dx = p12[0]+x1*t[0][0]-x2*t[1][0]
        dy = p12[1]+x1*t[0][1]-x2*t[1][1]
        dz = p12[2]+x1*t[0][2]-x2*t[1][2]

        dr = (dx**2+dy**2+dz**2)**1.5
        gm = (dx * t12[0] + dy * t12[1] + dz * t12[2]) / dr

        return gm
