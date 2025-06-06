# -----------------------------------------------------------------------------
# Copyright (c) 2023, 2024 Oracle and/or its affiliates.
#
# This software is dual-licensed to you under the Universal Permissive License
# (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl and Apache License
# 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose
# either license.
#
# If you elect to accept the software under the Apache License, Version 2.0,
# the following applies:
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# vector_async.py
#
# An asynchronous version of vector.py
#
# Demonstrates how to use the Oracle Database 23ai VECTOR data type.
# -----------------------------------------------------------------------------

import array
import asyncio
import sys

import oracledb
import sample_env


async def main():
    connection = await oracledb.connect_async(
        user=sample_env.get_main_user(),
        password=sample_env.get_main_password(),
        dsn=sample_env.get_connect_string(),
        params=sample_env.get_connect_params(),
    )

    # this script only works with Oracle Database 23.7 or later
    #
    # The VECTOR datatype was initially introduced in Oracle Database 23.4.
    # The BINARY vector format was introduced in Oracle Database 23.5.
    # The SPARSE vector format was introduced in Oracle Database 23.7.

    if sample_env.get_server_version() < (23, 7):
        sys.exit("This example requires Oracle Database 23.7 or later.")

    with connection.cursor() as cursor:
        # Single-row insert
        vector1_data_32 = array.array("f", [1.625, 1.5, 1.0])
        vector1_data_64 = array.array("d", [11.25, 11.75, 11.5])
        vector1_data_8 = array.array("b", [1, 2, 3])
        vector1_data_bin = array.array("B", [180, 150, 100])
        vector1_data_sparse64 = oracledb.SparseVector(
            30, [9, 16, 24], array.array("d", [19.125, 78.5, 977.375])
        )

        await cursor.execute(
            """insert into SampleVectorTab (v32, v64, v8, vbin, v64sparse)
               values (:1, :2, :3, :4, :5)""",
            [
                vector1_data_32,
                vector1_data_64,
                vector1_data_8,
                vector1_data_bin,
                vector1_data_sparse64,
            ],
        )

        # Multi-row insert
        vector2_data_32 = array.array("f", [2.625, 2.5, 2.0])
        vector2_data_64 = array.array("d", [22.25, 22.75, 22.5])
        vector2_data_8 = array.array("b", [4, 5, 6])
        vector2_data_bin = array.array("B", [40, 15, 255])
        vector2_data_sparse64 = oracledb.SparseVector(
            30, [3, 10, 12], array.array("d", [2.5, 2.5, 1.0])
        )

        vector3_data_32 = array.array("f", [3.625, 3.5, 3.0])
        vector3_data_64 = array.array("d", [33.25, 33.75, 33.5])
        vector3_data_8 = array.array("b", [7, 8, 9])
        vector3_data_bin = array.array("B", [0, 17, 101])
        vector3_data_sparse64 = oracledb.SparseVector(
            30, [8, 15, 29], array.array("d", [1.125, 200.5, 100.0])
        )

        rows = [
            (
                vector2_data_32,
                vector2_data_64,
                vector2_data_8,
                vector2_data_bin,
                vector2_data_sparse64,
            ),
            (
                vector3_data_32,
                vector3_data_64,
                vector3_data_8,
                vector3_data_bin,
                vector3_data_sparse64,
            ),
        ]

        await cursor.executemany(
            """insert into SampleVectorTab (v32, v64, v8, vbin, v64sparse)
               values (:1, :2, :3, :4, :5)""",
            rows,
        )

        # Query
        await cursor.execute("select * from SampleVectorTab")

        # Each non-sparse vector is represented as an array.array type.
        # Sparse vectors are represented as oracledb.SparseVector() instances
        async for row in cursor:
            print(row)


asyncio.run(main())
