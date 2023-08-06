from john import TestCase
from crelm import Factory
import importlib
import os.path


class Tdd(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tube = None
        cls._sut = None
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tube = None
        cls._sut = None
        return super().tearDownClass()

    @property
    def sut(self):
        self._ensure_sut()
        return self.__class__._sut
    
    def __init__(self, methodName: str):
        super().__init__(methodName)

    def _ensure_tube(self) -> None:
        if not self.__class__._tube:
            self.__class__._sut = None

            test_case_module = importlib.import_module(self.__module__)
            test_case_filename = test_case_module.__file__
            test_case_name = os.path.splitext(
                os.path.basename(test_case_filename))[0]

            c_filename = f'{test_case_name}.c'
            h_filename = f'{test_case_name}.h'

            self.__class__._tube = Factory().create_Tube(test_case_name) \
                .set_source_folder_relative(test_case_filename) \
                .add_source_file(c_filename) \
                .add_header_file(h_filename)

    def _ensure_sut(self):
        self._ensure_tube()
        if not self.__class__._sut:
            self.__class__._sut = self.__class__._tube.squeeze()

    def reset(self):
        self.__class__._sut = None