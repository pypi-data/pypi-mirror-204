# The Fast Marching Method
The *Fast Marching Method* (FMM), in its simplest form, can be used to compute the arrival times at grid cells for a monotonously expanding interface. One application of this method is to set the speed of the interface to one which enables computation of distance fields, where the closest distance to the interface is assigned to every cell in a grid. This repository contains an implementation of the FMM in arbitrary dimensions (actually two or more), although typical usage is most likely going to be 2D or 3D. The code is designed to be simple to incorporate into existing projects, and robustness has been prioritized over speed optimizations. All code in this repository is released under the [MIT license](https://en.wikipedia.org/wiki/MIT_License). If you have any comments or suggestions please feel free to make a pull request.

This note is divided into two major sections. First, we provide examples on how to use the code along with other practical details such as running the accompanying tests. Thereafter, we describe the technical choices that were made in the implementation with references to relevant literature.

## Usage
This section describes how to use the FMM implementation presented in this repository. First, we provide some examples on how to call these methods, together with some discussion related to valid inputs. Thereafter, we give instructions on how to run the accompanying tests. Note that there are also a lot of examples within the test code itself, which can be found in the [test folder](https://github.com/thinks/fast-marching-method/tree/master/test). 

The FMM implementation in this repository is contained in a single [header file](https://github.com/thinks/fast-marching-method/blob/master/include/thinks/fast_marching_method/fast_marching_method.hpp). This makes it very easy to add as a dependency to existing projects. Further, the code has no external dependencies other than the standard C++ libraries. All interfaces use standard types, such as `std::array` and `std::vector`. The code contains a fairly large number of `assert` statements, making it easier to debug when the `NDEBUG` preprocessor variable is not defined. However, the code runs very slowly in debug mode so input data set sizes may need to be adjusted accordingly.

### Methods
Most of the functions in the single [header file](https://github.com/thinks/fast-marching-method/blob/master/include/thinks/fast_marching_method/fast_marching_method.hpp) (which is all that needs to be included) are in `namespace detail` and should not be called directly. Instead, there is a single entry point provided by the `ArrivalTime` function. As the name suggests this function computes arrival times at grid cells. A conceptual example illustrates what is meant by this.

![alt text](https://github.com/thinks/fast-marching-method/blob/master/img/fmm_readme_concept.png "Conceptual example")

In the figure above, the green circle (_left_) was used as input to compute arrival times on a grid (_right_). Locations outside the circle have positive arrival times (or distances depending on interpretation), here shown in red. Similarly, locations inside the circle have negative arrival times, here shown in blue. The intensity gives the distance to the interface (i.e. circle boundary). This is why cells close to the interface appear black, since the red or blue component is small there. Next, we give an example demonstrating how to write code to generate an image similar to the one shown above.

The input to the `ArrivalTime` function is given as grid cells with known distances (or arrival times depending on interpretation). The following code snippet (full working code [here](https://github.com/thinks/fast-marching-method/blob/master/test/minimal_example.cpp) ) computes a low resolution version of the image shown above.

```cpp
namespace fmm = thinks::fast_marching_method;

// Select points close to a true circle
auto circle_boundary_indices = vector<array<int32_t, 2>>{
  {{5, 3}}, {{6, 3}}, {{7, 3}}, {{8, 3}}, {{9, 3}}, {{10, 3}}, {{4, 4}},
  {{5, 4}}, {{10, 4}}, {{11, 4}}, {{3, 5}}, {{4, 5}}, {{11, 5}}, {{12, 5}},
  {{3, 6}}, {{12, 6}}, {{3, 7}}, {{12, 7}}, {{3, 8}}, {{12, 8}}, {{3, 9}},
  {{12, 9}}, {{3, 10}}, {{4, 10}}, {{11, 10}}, {{12, 10}}, {{4, 11}},
  {{5, 11}}, {{10, 11}}, {{11, 11}}, {{5, 12}}, {{6, 12}}, {{7, 12}},
  {{8, 12}}, {{9, 12}}, {{10, 12}},
};

// Specify distances of such points to the true circle
auto circle_boundary_distances = vector<float>{
  0.0417385f, 0.0164635f, 0.0029808f, 0.0029808f, 0.0164635f, 0.0417385f,
  0.0293592f, -0.0111773f, -0.0111773f, 0.0293592f, 0.0417385f, -0.0111773f,
  -0.0111773f, 0.0417385f, 0.0164635f, 0.0164635f, 0.0029808f, 0.0029808f,
  0.0029808f, 0.0029808f, 0.0164635f, 0.0164635f, 0.0417385f, -0.0111773f,
  -0.0111773f, 0.0417385f, 0.0293592f, -0.0111773f, -0.0111773f, 0.0293592f,
  0.0417385f, 0.0164635f, 0.0029808f, 0.0029808f, 0.0164635f, 0.0417385f
};

auto grid_size = array<size_t, 2>{{16, 16}};
auto grid_spacing = array<float, 2>{{1.f/16, 1.f/16}};
auto uniform_speed = 1.f;

auto arrival_times = fmm::SignedArrivalTime(
  grid_size,
  circle_boundary_indices,
  circle_boundary_distances,
  fmm::UniformSpeedEikonalSolver<float, 2>(grid_spacing, uniform_speed));
```

First, we define our input, the cell coordinates for which we have known distances. These are stored in two separate lists, one for the coordinates of the cells (`circle_boundary_indices`) and one for the corresponding distances (`circle_boundary_distances`). Normally, these values would of course not be hard-coded, but rather generated by some function. Thereafter, we specify the size (`grid_size`) and dimensions (`grid_spacing`) of the grid. Here the grid dimensions are set so that the domain is [0, 1] in each dimension. In order to be able to interpret the arrival times as euclidean distance, a uniform speed of one is set for the entire grid (`uniform_speed`). The speed is passed to an Eikonal solver that determines the method used to propagate distances. Eikonal solvers will be discussed in further detail in the following section. The resulting image is shown below.

![alt text](https://github.com/thinks/fast-marching-method/blob/master/img/fmm_readme_input_values.png "Code example")

Boundary condition cells with known distances are shaded darker grey in the left image. Known input values may be interpreted as radii that intersect the input shape. We note that negative distances are used when the cell center is inside the circle. In the next section we discuss the use of Eikonal solvers, which allow easy customization of the algorithm while re-using the basic ideas.

### Eikonal Solvers
The basic idea of the FMM algorithm is to propagate given information at known locations to other locations in a numerically reasonable way. Now, the way that the FMM algorithm handles this is by assuming that information close to known locations is more reliable than information further away, which is why it is said to be a propagating method. Even though the basic propagation scheme remains the same there is still flexibility when it comes to the details of how to compute information at new locations. This is what Eikonal solvers are used for in this implementation. 

Up to this point we have assumed the speed of the propagating interface to be uniformly one, which is convenient since it allows us to intuitively interpret arrival times as distance. However, the FMM allows arbitrary positive speeds and does not require the speed to be the same for each cell. Also, since propagating information requires partial derivates it is possible to achieve better accuracy using higher order discretization schemes. This leads to the following types of basic Eikonal solvers:
* `UniformSpeedEikonalSolver`
* `HighAccuracyUniformSpeedEikonalSolver`
* `VaryingSpeedEikonalSolver`
* `HighAccuracyVaryingSpeedEikonalSolver`
* `DistanceEikonalSolver` (from Bridson book, REF!!!)

These types are provided in the same [header file](https://github.com/thinks/fast-marching-method/blob/master/include/thinks/fast_marching_method/fast_marching_method.hpp) as the rest of the code. It is of course possible to extend these further with user-defined solvers. Example usages of the different solver types are shown in the image below.

![alt text](https://github.com/thinks/fast-marching-method/blob/master/img/fmm_readme_eikonal_solvers.png "Eikonal solvers")


### Input Validation


### Tests
In order to run the tests you need to have [CMake](https://cmake.org/) installed. The tests are implemented in the [Google Test](https://github.com/google/googletest) framework, which is included as part of this repository. 

Running the tests is simple. In a terminal do the following:

```bash
$ cd d:
$ git clone git@github.com:/thinks/fast-marching-method.git D:/fmm
$ mkdir fmm-build
$ cd fmm-build
$ cmake ../fmm/test -DCMAKE_BUILD_TYPE=Release
$ cmake --build . 
$ ctest
```

In order, the following is being done:
* Clone the source code to a directory `D:/fmm`.
* Create an out-of-source build directory `fmm-build`.
* Create the default project files for your machine in the build directory (change `Release` to `Debug` for a debug build).
* Builds the tests.
* Runs the tests. 

If the tests pass you should see something like:

```
Test project D:/fmm-build
    Start 1: fast-marching-method-test
1/1 Test #1: fast-marching-method-test ........     Passed      0.33 sec

100% tests passed, 0 tests failed out of 1

Total test time (real) =    0.35 sec

```

For more detailed test output you can run the test executable directly:

```
$ D:/fmm-build/fast-marching-method-test.exe
```

## Technical Details
This section describes our FMM implementation from a more technical perspective. Relevant implementation details are discussed and references are provided when applicable. A high degree of familiarity with the FMM is assumed here. For those who wish learn more about the basics of the FMM we recommend **[3]** as a good starting point. Finally, possible directions for future work together with references for additional material on the FMM are given.

### Simplified Fast Marching Method
A key part of the FMM algorithm is the specific order in which cells are visited during arrival time propagation. Achieving this specific order requires maintaining a priority queue of tentative arrival times for cells during propagation. Since the tentative arrival time at a cell can be re-evaluated several times a cell may change position in the priority queue. The operation of finding and moving a cell in the priority queue is relatively expensive and, moreover, requires a specialized data structure. In **[4]**, Jones et al. observe that increasing the tentative arrival time at a cell during recomputation is detrimental to the final result. They therefore propose a somewhat simpler propagation scheme that allows cells to appear multiple times in the priority queue. This alleviates the need for finding and moving cells in the queue at the small cost of having to check if a cell has already been finalized when it appears at the front of the queue. Pseudo-code for the simplified FMM is as follows **[4]**:

```
Extract cell with smallest tentative arrival time from queue
If cell is not finalized
    Finalize the cell
    Recompute arrival times for unfinalized neighbor cells
    Insert neighbor cells in queue
```

Note that this scheme does not require updating existing elements in the priority queue. Instead multiple tentative arrival times may be added for the same cell. Only the smallest tentative arrival time determines when a cell is finalized, effectively ignoring larger tentative arrival times for that cell. This means that a standard priority queue may be used instead of some specialized structure that needs to accommodate updates of existing elements.

### High Accuracy Fast Marching Method
At the core of the FMM is the discrete approximation of derivatives used when solving the [eikonal equation](https://en.wikipedia.org/wiki/Eikonal_equation). Commonly, first order approximations are used, but it is sometimes possible to achieve better results using higher order discretization schemes. In **[6]** Sethian describes a second order discretization scheme referred to as *High Accuracy FMM*. Using higher order discretization has the potential to make the FMM significanly more accurate than its first order counterpart. A simple example illustrates this.

![alt text](https://github.com/thinks/fast-marching-method/blob/master/img/fmm_readme_point_source_error.png "Point source error")

Starting from a point source at the middle of the image (where arrival time is zero), arrival times were computed using both regular (first order) FMM and high accuracy FMM. A uniform speed of one over the entire domain was used here. Visually it is quite difficult to tell the difference other than that the dark area around the point source appears slightly less axis-aligned in the high accuracy version. However, the differences become apparent when we visualize errors. We note that errors for regular FMM are overall relatively high except along the grid axes. The pattern is similar for high accuracy FMM, but the areas of lower error extend at a wider angle from the grid axes. Since the high accuracy discretization scheme uses a larger cell neighborhood it is important that the initial boundary cells are able to provide such information. Otherwise first order derivatives will be used for the initial neighbors and those inaccuracies will propagate to the rest of the domain. In the example above boundary values were given for the 8-neighborhood of the cell containing the point source when computing the high accuracy arrival times. While such dilated boundaries are trivial to provide in some scenarios it may not be in others. This is a problem that needs to be solved in the steps that generate input to the FMM procedure and is not directly related to the work herein. 

In **[3]** Baerentzen provides numbers for the max and mean error of his implementation in a scenario similar to the one we use above. His numbers are given for a point source at the center of a 3D grid where max and mean error where computed within a radius of 20 cells. A radial cutoff is used to avoid directional bias. The reported max and mean errors for regular FMM are 1.48 and 0.89 voxel units (i.e. the distance between two cell centers, assuming square cells), respectively. For high accuracy FMM these numbers fall to 0.27 and 0.07 voxel units, respectively. We repeated this experiment for the implementation in this repository and found that our result were extremely close to those reported in **[3]**. In fact, there are unit tests in place to assure that the accuracy does not fall below these levels.

Finally, we use the elegant formulations provided by Rickett and Fomel in **[2]** for accumulating quadratic coefficients when solving the [eikonal equation](https://en.wikipedia.org/wiki/Eikonal_equation). Their framework enables a simple way of using second order derivatives when the cell neighborhood allows it and otherwise falling back to first order derivatives. Interestingly, the propagation scheme, i.e. the order in which cells are updated, is independent of how we choose to solve the [eikonal equation](https://en.wikipedia.org/wiki/Eikonal_equation).

### Morphological Sign Computation
In some applications of the FMM boundary cells represent point sources and only positive travel times are of interest. The field of seismic study (e.g. **[7]**) is a good example of this. In these cases boundary cells form filled shapes and there is no concept of inside. In other words, arrival times are only propagated outward from solid shapes. However, in the level set community it is often desirable to convert shapes from explicit representations, such as triangle meshes, to implicit representations, i.e. distance fields. Computing distance fields using the FMM is easily achieved by settings a uniform speed equal to one on the entire domain, which allows arrival time to be interpreted as distance. It is common to use signed distance fields, where the inside of a shape has negative distance values. As discussed below, a simple trick is required to achieve correct inside distances.

![alt text](https://github.com/thinks/fast-marching-method/blob/master/img/fmm_readme_inside_outside.png "Sign computation")

We wish to create a signed distance field from the green circle. Cell values are shown as circles since we can interpret them as radii representing the minimum distance to the interface (points on the green circle). From the definition of distance fields we know that cell circles are tangential to the green circle at one or more locations. The concept of negative distance is only used to distinguish between inside-outside, geometrically the tangential property applies to absolute values.

For simplicity we consider only a few cells in a single grid row. In the top illustration we note the issue of dual contouring, where inside (dashed circles) and outside cells consider the interface to be at different locations. Dual contouring happens because the FMM algorithm is symmetric in the sense that propagated values move away from the interface. 

In the bottom version we show the correct distance values. As mentioned briefly in **[8]**, the dual contouring issue can be resolved by sign-flipping the boundary values while propagating inward. Note that inside values are positive while propagating and these cells need to be manually sign-flipped after inward propagation finishes. Now, given that we need to distinguish between inward and outward propagation, how do we know if a boundary cell neighbor is on the inside or outside?

A morphological approach is used to determine the inside and outside areas of the shape described by the given boundary cells. First, we perform a morphological dilation of the boundary cells using the vertex neighborhood, i.e. all cells that share a vertex with a boundary cell are tagged as being part of a dilation band. Next, we perform connected component labelling of the dilation band cells. This results in one or more separate dilation bands. Every shape has an outer dilation band and in the presence of multiple dilation bands, the outer dilation band always has the largest bounding box. Other dilation bands are referred to as inner dilation bands and we know that these cells are on the inside of the shape. The image below illustrates these ideas.

![alt text](https://github.com/thinks/fast-marching-method/blob/master/img/fmm_readme_dilation_bands.png "Inside/outside")

The simplest case is when the given boundary cells form a single connected component. There may be an arbitrary number of dilation bands, but inside and outside can always be determined without ambiguities. Note that the input grid is padded by one cell in each direction while computing the dilation bands. The reasoning behind this is that non-closed shapes should not have insides, which would otherwise happen. In the case of two or more connected boundary components there is the possibility that one of the components is contained by one of the other components. If this is the case there is an ambiguity regarding inside and outside, since the contained component's outside will be considered to be inside by the containing component. Interestingly, the outsides of separate components will at some point interact with each other, while insides will never interact with dilation band cells from any other dilation band. In order to determine if a component is contained within another we flood fill all inside regions and check for the existence of boundary cells.


Does not work well in 1D!

### Code Design

[Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)

references for further reading

### Future Work
* Termination criteria for narrow band marching.
* Comparison with fast sweeping method and vector distance transforms [Ref: VCVDT].


### References
**[1]** J.A. Sethian. A fast marching level set method for monotonically advancing fronts. *Proceeding of the National Academy of Sciences of the USA - Paper Edition*, 93(4):1591-1595, 1996.

**[2]** J. Rickett and S. Fomel. Short note: A second-order fast marching eikonal solver. *Technical Report, Stanford Exploration Project*, 2000.

**[3]** J.A. Baerentzen. On the implementation of fast marching methods for 3D lattices. *Technical Report. IMM-TR-2001-13*, 2001.

**[4]** M.W. Jones, J.A. Baerentzen, and M. Sramek. 3D Distance Fields: A Survey of Techniques and Applications. *IEEE Transactions on Visualization and Computer Graphics*, 12(4):581-599, July/August 2006.

**[5]** R. Bridson. Fluid Simulation for Computer Graphics. *CRC Press*, 2015.

**[6]** J.A. Sethian. Level set methods and fast marching methods. *Cambridge Monographs on Applied and Computational Mathematics*, Cambridge University Press, second edition, 1999.

**[7]** N. Rawlinson, M. de Kool, and M. Sambridge. Seismic wavefront tracking in 3D heterogeneous media: applications with multiple data classes. *Exploration Geophysics*, 37(4):322–330, 2006.

**[8]** S. Osher and R. Fedkiw. Level Set Methods and Dynamic Implicit Surfaces. *Springer*, 2003













