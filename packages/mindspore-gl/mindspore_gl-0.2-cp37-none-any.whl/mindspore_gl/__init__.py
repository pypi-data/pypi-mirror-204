# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Module init"""
from .version import __version__, mindspore_version_check
mindspore_version_check()

# pylint: disable=C0413
from .parser import *
from .nn import *
from .graph import *
from .sampling import *
from .dataset import *
from .dataloader import *
from .utils import *

__all__ = parser.__all__
__all__.extend(nn.__all__)
__all__.extend(__version__)
