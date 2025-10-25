#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

#modified by @Keloyi531 (Oct 2025), updated for RTX 5090 / CUDA 12.8 compatibility

from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension
import os

os.path.dirname(os.path.abspath(__file__))

setup(
    name="diff_gaussian_rasterization",
    packages=['diff_gaussian_rasterization'],
    ext_modules=[
        CUDAExtension(
            name="diff_gaussian_rasterization._C",
            sources=[
                "cuda_rasterizer/rasterizer_impl.cu",
                "cuda_rasterizer/forward.cu",
                "cuda_rasterizer/backward.cu",
                "rasterize_points.cu",
                "ext.cpp"
            ],
            extra_compile_args={
                "cxx": ["/std:c++17",
        "/permissive-",
        "/EHsc",
        "/bigobj",
        "/MD",
        "/Zc:__cplusplus",
        "/Zc:preprocessor"],
                "nvcc": ["-gencode=arch=compute_120,code=sm_120",   # or 'code=compute_120' as PTX-only fallback
        "-Xcompiler=/std:c++17,/permissive-,/EHsc,/bigobj,/MD,/Zc:__cplusplus,/Zc:preprocessor",
        "--expt-relaxed-constexpr",
        "-DTORCHDYNAMO_DISABLE=1",
        "-I" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "third_party/glm/"),
                ],
            },
        )
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)
