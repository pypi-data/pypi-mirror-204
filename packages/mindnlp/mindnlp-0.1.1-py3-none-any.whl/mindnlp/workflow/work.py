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
"""
The meta classs of work in Workflow.
"""

# pylint: disable=no-member

import abc
import os
from abc import abstractmethod

from mindnlp.configs import DEFAULT_ROOT
from mindnlp.utils import cache_file


class Work(metaclass=abc.ABCMeta):
    """
    The meta classs of work in Workflow. The meta class has the five abstract function,
        the subclass need to inherit from the meta class.

    Args:
        work(string): The name of work.
        model(string): The model name in the work.
        kwargs (dict, optional): Additional keyword arguments passed along to the specific work.
    """

    def __init__(self, model, work, **kwargs):
        self.model = model
        self.work = work
        self.kwargs = kwargs
        self._usage = ""
        self._model = None
        # The root directory for storing Workflow related files, default to ~/.mindnlp.
        self._home_path = self.kwargs["home_path"] if "home_path" in self.kwargs else DEFAULT_ROOT
        self._work_flag = self.kwargs["work_flag"] if "work_flag" in self.kwargs else self.model
        self.from_hf_hub = kwargs.pop("from_hf_hub", False)

        if "work_path" in self.kwargs:
            self._work_path = self.kwargs["work_path"]
            self._custom_model = True
        else:
            self._work_path = os.path.join(
                self._home_path, "workflow", self.work, self.model)

        if not self.from_hf_hub:
            pass

    @abstractmethod
    def _construct_model(self, model):
        """
        Construct the inference model for the predictor.
        """

    @abstractmethod
    def _construct_tokenizer(self, model):
        """
        Construct the tokenizer for the predictor.
        """

    @abstractmethod
    def _preprocess(self, inputs, padding=True, add_special_tokens=True):
        """
        Transform the raw text to the model inputs, two steps involved:
           1) Transform the raw text to token ids.
           2) Generate the other model inputs from the raw text and token ids.
        """

    @abstractmethod
    def _run_model(self, inputs):
        """
        Run the work model from the outputs of the `_tokenize` function.
        """

    @abstractmethod
    def _postprocess(self, inputs):
        """
        The model output is the logits and pros,
        this function will convert the model output to raw text.
        """

    def _get_graph_model_name(self):
        """
        Get the graph model name.
        """
        return ''

    def _check_work_files(self):
        """
        Check files required by the work.
        """
        for file_id, file_name in self.resource_files_names.items():
            path = os.path.join(self._work_path, file_id, file_name)
            cache_dir = os.path.join(self._work_path, file_id)
            url = self.resource_files_urls[self.model][file_id][0]
            md5 = self.resource_files_urls[self.model][file_id][1]

            downloaded = True
            if not os.path.exists(path=path):
                downloaded = False
            if not downloaded:
                cache_file(filename=file_name, cache_dir=cache_dir,
                           url=url, md5sum=md5)

    def _check_predictor_type(self):
        """
        Check the predictor type.
        """

    def _prepare_graph_mode(self):
        """
        Construct the input data and predictor in the MindSpore graph mode.
        """

    def _prepare_onnx_mode(self):
        """
        Prepare the onnx model.
        """

    def _get_inference_model(self):
        """
        Return the inference program, inputs and outputs in graph mode.
        """

    def _check_input_text(self, inputs):
        """
        Check whether the input text meet the requirement.
        """
        inputs = inputs[0]
        if isinstance(inputs, str):
            if len(inputs) == 0:
                raise ValueError("Invalid inputs, input text should not be empty text, \
                    please check your input.")
            inputs = [inputs]
        elif isinstance(inputs, list):
            if not (isinstance(inputs[0], str) and len(inputs[0].strip()) > 0):
                raise TypeError(
                    "Invalid inputs, input text should be list of str, \
                        and first element of list should not be empty text."
                )
        else:
            raise TypeError(
                f"Invalid inputs, input text should be str or list of str, \
                    but type of {type(inputs)} found!"
            )
        return inputs

    def _auto_splitter(self, input_texts, max_text_len, bbox_list=None, split_sentence=False):
        """
        Split the raw texts automatically for model inference.
        """

    def _auto_joiner(self, short_results, input_mapping, is_dict=False):
        """
        Join the short results automatically and generate
        the final results to match with the user inputs.
        """

    def help(self):
        """
        Return the usage message of the current work.
        """
        print(f"Examples:\n{self._usage}")

    def __call__(self, *args):
        inputs = self._preprocess(*args)
        outputs = self._run_model(inputs)
        results = self._postprocess(outputs)
        return results
