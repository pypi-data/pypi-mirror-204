from .Test import Test

class EmptyTest(Test):
    def __init__(self, filename, node, lineno):
        super().__init__(filename, node, None, None, lineno)

    
    def get_tag(self):
        return "orange"
    
    def get_status(self):
        return super()._EMPTY_STATUS
    
    def __str__(self):
        from thonnycontrib.utils import create_node_representation
        empty_node = create_node_representation(self.node)
        return "No test detected for: %s" % (empty_node)
