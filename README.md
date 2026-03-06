# India Census Data Dashboard

An interactive data visualization dashboard built with Streamlit and Plotly to explore demographic insights across Indian states and districts.

## Live Demo

**[View Live App](https://dxzznlapyf26p6l8upgtdc.streamlit.app/)**

## Features

- **Interactive Map Visualization**: Explore census data geographically with scatter maps
- **State/District Selection**: View data for Overall India or drill down to specific states
- **Customizable Parameters**: Choose primary (marker size) and secondary (marker color) parameters
- **Multiple Color Schemes**: Select from Viridis, Plasma, Inferno, Turbo, Blues, Reds, or Greens
- **Key Statistics**: View summary metrics including population, literacy rate, sex ratio, and internet access
- **Detailed Data Table**: Expandable view of filtered data with sorting

## Available Parameters

| Parameter | Description |
|-----------|-------------|
| Population | Total population count |
| Literacy Rate | Percentage of literate population |
| Sex Ratio | Females per 100 males |
| Internet Access | Households with internet connectivity |

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Censusdashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to `http://localhost:8501`

## Requirements

- Python 3.8+
- Streamlit
- Plotly
- Pandas
- NumPy

## Project Structure

```
Censusdashboard/
├── app.py              # Main Streamlit application
├── india.csv           # Census dataset
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Dataset

The dashboard uses Indian census data (`india.csv`) containing demographic information for districts across all states, including:
- Geographic coordinates (Latitude, Longitude)
- Population statistics
- Literacy data
- Sex ratio
- Internet connectivity metrics

## Usage

1. **Select Region**: Choose "Overall India" or a specific state from the sidebar
2. **Configure Parameters**: Select primary parameter (controls marker size) and secondary parameter (controls marker color)
3. **Choose Color Scheme**: Pick a color palette for the visualization
4. **Generate Visualization**: Click the button to render the map and statistics

## Technologies Used

- **Streamlit**: Web application framework
- **Plotly Express**: Interactive visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations

## License

This project is open source and available under the MIT License.
