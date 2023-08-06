# Auteur : Réda ID-TALEB

from .FailedTest import FailedTest

class FailedWhenExceptionExpectedTest(FailedTest):
    def __init__(self, filename:str, node, tested_line, expected_result, lineno, failure_message):
        super().__init__(filename, node, tested_line, expected_result, lineno, obtained_result=None)
        self.failure_message = failure_message
    
    def get_detail_failure(self):
        return self.failure_message  
