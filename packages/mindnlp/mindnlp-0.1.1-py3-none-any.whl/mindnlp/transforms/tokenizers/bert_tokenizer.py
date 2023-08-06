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
BertTokenizer
"""

import numpy as np
from mindspore.dataset.transforms.transforms import PyTensorOperation
from mindspore.dataset.text.transforms import Implementation
from tokenizers.implementations import BertWordPieceTokenizer

class BertTokenizer(PyTensorOperation):
    """
    Tokenizer used for Bert text process.

    Args:
        vocab (Vocab): Vocabulary used to look up words.
        lower_case (bool, optional): Whether to perform lowercase processing on the text. If True, will fold the
            text to lower case. Default: True.
        py_transform (bool, optional): Whether use python implementation. Default: False.

    Raises:
        TypeError: If `lower_case` is not of type bool.
        TypeError: If `py_transform` is not of type bool.
        RuntimeError: If dtype of input Tensor is not str.

    Examples:
        >>> from mindspore.dataset import text
        >>> from mindnlp.dataset.transforms import BertTokenizer
        >>> vocab_list = ["床", "前", "明", "月", "光", "疑", "是", "地", "上", "霜", "举", "头", "望", "低",
              "思", "故", "乡","繁", "體", "字", "嘿", "哈", "大", "笑", "嘻", "i", "am", "mak",
              "make", "small", "mistake", "##s", "during", "work", "##ing", "hour", "😀", "😃",
              "😄", "😁", "+", "/", "-", "=", "12", "28", "40", "16", " ", "I", "[CLS]", "[SEP]",
              "[UNK]", "[PAD]", "[MASK]", "[unused1]", "[unused10]"]
        >>> vocab = text.Vocab.from_list(vocab_list)
        >>> tokenizer_op = BertTokenizer(vocab=vocab, lower_case=True)
        >>> text = "i make a small mistake when i\'m working! 床前明月光😀"
        >>> tokenized_text = tokenizer_op(text)

    """

    # @check_decode
    def __init__(self, vocab, lower_case:bool = True, return_token = False):
        super().__init__()
        self.tokenizer = BertWordPieceTokenizer(vocab=vocab.vocab(), lowercase=lower_case)
        self.return_token = return_token
        self.implementation = Implementation.PY

    def __call__(self, text_input):
        """
        Call method for input conversion for eager mode with C++ implementation.
        """
        if isinstance(text_input, str):
            text_input = np.array(text_input)
        elif not isinstance(text_input, np.ndarray):
            raise TypeError(
                f"Input should be a text line in 1-D NumPy format, got {type(text_input)}.")
        return super().__call__(text_input)

    def execute_py(self, text_input):
        """
        Execute method.
        """
        return self._execute_py(text_input)

    def _execute_py(self, text_input):
        """
        Execute method.
        """
        text = self._convert_to_unicode(text_input)
        output = self.tokenizer.encode(text)
        if self.return_token is True:
            return np.array(output.tokens)
        return np.array(output.ids)

    def _convert_to_unicode(self, text_input):
        """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
        if isinstance(text_input, str):
            return text_input
        if isinstance(text_input, bytes):
            return text_input.decode("utf-8", "ignore")
        if isinstance(text_input, np.ndarray):
            if text_input.dtype.type is np.bytes_:
                text_input = np.char.decode(text_input, "utf-8")
            return str(text_input)
        raise ValueError(f"Unsupported string type: {type(text_input)}, {text_input.dtype}")
