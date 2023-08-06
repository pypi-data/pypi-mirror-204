from .l1test_runner import L1TestRunner

# Ceci est une implémentation de création d'un singleton pour L1TestRunner
_l1test_runner: L1TestRunner = None

def get_l1test_runner() -> L1TestRunner:
    """
    If there's no `L1TestRunner` instance creates one and returns it, 
    otherwise returns the current `L1TestRunner` instance.
    """
    return L1TestRunner() if not _l1test_runner else _l1test_runner