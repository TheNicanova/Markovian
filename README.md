# OptimalStopping

OptimalStopping is a Python repository designed to be a playground for testing optimal stopping algorithms using Monte Carlo methods. It aims to facilitate the design and testing of pricing algorithms through a modular approach, with a focus on evaluating their performance under different sample sizes and visually interpreting the results.

The repository is organized into two main components: inner steps and outer steps. The inner steps involve generating sample price trajectories and estimating option prices, while the outer steps deal with evaluating algorithm performance and visualizing results.

## Key Components

### Inner Steps

1. **UnderlyingModels**: A subpackage responsible for sampling price trajectories. This module allows users to generate synthetic price data based on various underlying models.
2. **PricingModels**: A subpackage dedicated to estimating option prices using the sampled price trajectories. Users can experiment with different pricing algorithms to determine their effectiveness in the optimal stopping problem.

### Outer Steps

1. **Performance Estimation**: Assess the performance of the pricing algorithms by testing their accuracy under different sample sizes. This step helps users identify the most effective algorithms and understand the trade-offs between accuracy and computational resources.
2. **Visualization**: Generate various plots to visually interpret the performance of the tested algorithms. These visualizations can provide valuable insights into algorithm behavior and help users make informed decisions about which methods to pursue further.

OptimalStopping is intended for researchers, quantitative analysts, and anyone interested in exploring the application of Monte Carlo methods in optimal stopping problems.