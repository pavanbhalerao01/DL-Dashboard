"""
Utility package for deep learning model comparison
"""

__version__ = "1.0.0"
__author__ = "DL Research Team"

from .generate_results import (
    create_results_database,
    create_comparison_dataframe,
    save_results,
)

from .visualizations import (
    create_all_visualizations,
    plot_accuracy_by_algorithm,
    plot_optimizer_comparison,
    plot_learning_rate_impact,
)

__all__ = [
    'create_results_database',
    'create_comparison_dataframe',
    'save_results',
    'create_all_visualizations',
    'plot_accuracy_by_algorithm',
    'plot_optimizer_comparison',
    'plot_learning_rate_impact',
]
