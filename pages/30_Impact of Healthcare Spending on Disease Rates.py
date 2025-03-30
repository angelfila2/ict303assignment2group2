import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Suppress warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Page configuration
st.set_page_config(page_title="Immunization & Disease Analysis", layout="wide")
st.title("📊 Immunization Expenditure & Infectious Disease Analysis")
st.markdown("""
This dashboard examines the correlation between **vaccination costs** and **cases of infectious diseases** over time in various nations.  
We seek to determine whether **greater investment in healthcare** results in a **decrease in disease prevalence** by analyzing trends **globally** and specifically in **ASEAN**.

### 🔍 The dashboard provides:
""")

st.markdown("""
✅ **Global trends** in disease burden and vaccination spending
""")

st.markdown("""
✅ **ASEAN-specific analysis** to identify regional differences
""")

st.markdown("""
✅ **Correlation insights** to evaluate how immunization funding affects disease control 
""")

# Define helper functions
def create_metrics(col1, col2, col3, metric1, value1, metric2, value2, metric3, value3):
    with col1:
        st.metric(metric1, value1)
    with col2:
        st.metric(metric2, value2)
    with col3:
        st.metric(metric3, value3)

def format_large_number(num):
    """
    Format large numbers as millions (M) or billions (B) for better readability.
    """
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return f"{num:.2f}"

def create_filters(min_year, max_year, df, key_prefix, disease_filter=True, region_filter=False, top_n_filter=False):
    filters = {}

    filter_cols = st.columns(3)
    with filter_cols[0]:
        filters['year_range'] = st.slider(
            "Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            key=f"{key_prefix}_year_slider"
        )

    with filter_cols[1]:
        if top_n_filter:
            filters['top_n'] = st.slider("Show Top N Countries",
                                         min_value=5, max_value=20, value=10,
                                         key=f"{key_prefix}_top_n_slider")

    with filter_cols[2]:
        if disease_filter and 'SUBJECT' in df.columns:
            disease_types = sorted(df['SUBJECT'].unique())
            filters['disease'] = st.selectbox(
                "Disease Type",
                options=["All"] + disease_types,
                key=f"{key_prefix}_disease_filter"
            )
        else:
            filters['disease'] = "All"

    if region_filter and 'REGION' in df.columns:
        regions = sorted(df['REGION'].unique())
        filters['regions'] = st.multiselect(
            "Select Regions",
            options=["All"] + regions,
            default="All",
            key=f"{key_prefix}_region_filter"
        )
    else:
        filters['regions'] = ["All"]

    return filters


def filter_data(df, filters, countries=None):
    filtered_df = df.copy()

    # Filter by year range
    filtered_df = filtered_df[
        (filtered_df['YEAR'] >= filters['year_range'][0]) &
        (filtered_df['YEAR'] <= filters['year_range'][1])
        ]

    # Filter by countries if provided
    if countries:
        filtered_df = filtered_df[filtered_df['COUNTRYNAME'].isin(countries)]

    # Filter by disease type if selected
    if filters.get('disease') != "All" and 'SUBJECT' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['SUBJECT'] == filters['disease']]

    # Filter by region if selected
    if filters.get('regions') != ["All"] and 'REGION' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['REGION'].isin(filters['regions'])]

    return filtered_df


def plot_interactive_bar(data, x, y, title, xlabel, ylabel):
    """Create an interactive bar chart with plotly"""
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        labels={x: xlabel, y: ylabel},
        hover_data={x: True, y: ':.2f'}
    )

    # Customize hover template with formatted values
    hovertemplate = f"<b>%{{x}}</b><br>{ylabel}: %{{customdata}}<extra></extra>"

    # Create formatted values for hover text
    customdata = [format_large_number(val) for val in data[y]]

    # Update traces with custom hover template
    fig.update_traces(
        customdata=customdata,
        hovertemplate=hovertemplate
    )

    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        hoverlabel=dict(
            bgcolor="black",
            font_size=12,
            font_family="Arial"
        ),
        hovermode="closest"
    )

    return fig


def plot_interactive_line(data, x, y, title, xlabel, ylabel, color=None, line_group=None):
    """Create an interactive line chart with plotly"""
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        line_group=line_group,
        labels={x: xlabel, y: ylabel},
        hover_data={x: True, y: ':.2f'},
        markers=True
    )

    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        legend_title_text=color if color else "",
        hoverlabel=dict(
            bgcolor="black",
            font_size=12,
            font_family="Arial"
        ),
        hovermode="closest"
    )

    return fig

def format_number(num):
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.2f}K"
    else:
        return f"{num:.2f}"

def calculate_correlations(df, group_by='COUNTRYNAME'):
    corr_df = df.groupby(group_by).apply(
        lambda x: x['IMMUNISATION_EXPENDITURE'].corr(x['DISEASE_CASES'])
    ).reset_index()
    corr_df.columns = ['Country', 'Correlation']
    return corr_df.sort_values('Correlation')


def plot_scatter_with_regression(df, country=None):
    """Create a scatter plot with regression line to visualize correlation"""
    if country:
        plot_df = df[df['COUNTRYNAME'] == country].copy()
        title = f"Correlation Analysis for {country}"
    else:
        plot_df = df.copy()
        title = "Global Correlation Analysis"

    # Create the scatter plot with trend line
    fig = px.scatter(
        plot_df,
        x='IMMUNISATION_EXPENDITURE',
        y='DISEASE_CASES',
        color='COUNTRYNAME' if not country else None,
        trendline='ols',
        title=title,
        labels={
            'IMMUNISATION_EXPENDITURE': 'Immunization Expenditure',
            'DISEASE_CASES': 'Disease Cases'
        }
    )

    # Update layout for better readability
    fig.update_layout(
        xaxis_title="Immunization Expenditure",
        yaxis_title="Disease Cases",
        hoverlabel=dict(
            bgcolor="black",
            font_size=12,
            font_family="Arial"
        ),
        hovermode="closest"
    )

    # Add annotations for correlation coefficient
    if country:
        corr = plot_df['IMMUNISATION_EXPENDITURE'].corr(plot_df['DISEASE_CASES'])
        fig.add_annotation(
            x=0.05, y=0.95,
            xref="paper", yref="paper",
            text=f"Correlation: {corr:.3f}",
            showarrow=False,
            font=dict(size=14, color="black"),
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor="black",
            borderwidth=1,
            borderpad=4
        )

    return fig

@st.cache_data
def load_data():
    # Replace with your actual file paths
    file1 = file1 = "data/Immunization_expenditure.csv"
    file2 = "data/Infectious_Disease.csv"

    df_immunization = pd.read_csv(file1, encoding='ISO-8859-1')
    df_disease = pd.read_csv(file2)
    return df_immunization, df_disease


# Load and preprocess data
df_immunization, df_disease = load_data()

# Data Preprocessing
df_immunization['VALUE'] = pd.to_numeric(df_immunization['VALUE'], errors='coerce')
df_immunization_vacc = df_immunization[df_immunization['INDCODE'] == 'FIN_GVT_VACC'].copy()
df_immunization_grouped = \
    df_immunization_vacc.dropna(subset=['VALUE']).groupby(['COUNTRYNAME', 'YEAR'], as_index=False)['VALUE'].sum()
df_immunization_grouped.rename(columns={"VALUE": "IMMUNISATION_EXPENDITURE"}, inplace=True)

df_disease.columns = df_disease.columns.str.strip().str.upper()
df_disease.rename(columns={"PERIOD": "YEAR", "LOCATION": "COUNTRYNAME", "FACTVALUENUMERIC": "DISEASE_CASES"},
                  inplace=True)

df_merged = pd.merge(df_immunization_grouped, df_disease, on=["YEAR", "COUNTRYNAME"], how="inner")
df_merged = df_merged.dropna(subset=['DISEASE_CASES'])
df_merged['YEAR'] = pd.to_numeric(df_merged['YEAR'], errors='coerce')

# Define ASEAN countries
asean_countries = ["Brunei", "Cambodia", "Indonesia", "Laos", "Malaysia",
                   "Myanmar", "Philippines", "Singapore", "Thailand", "Vietnam"]

# Calculate preventive and treatment spending percentages
df_spending = df_immunization_grouped.copy()
df_spending['PREVENTIVE_SPENDING'] = df_spending['IMMUNISATION_EXPENDITURE'] * 0.4  # Placeholder
df_spending['TREATMENT_SPENDING'] = df_spending['IMMUNISATION_EXPENDITURE'] * 0.6  # Placeholder
df_spending['TOTAL_SPENDING'] = df_spending['PREVENTIVE_SPENDING'] + df_spending['TREATMENT_SPENDING']
df_spending['PREVENTIVE_SPENDING_PERCENT'] = (df_spending['PREVENTIVE_SPENDING'] / df_spending['TOTAL_SPENDING']) * 100
df_spending['TREATMENT_SPENDING_PERCENT'] = (df_spending['TREATMENT_SPENDING'] / df_spending['TOTAL_SPENDING']) * 100

# Create tabs for different sections
global_tab, asean_tab = st.tabs(["Global Overview", "ASEAN Focus"])

# Global Overview Tab
with global_tab:
    st.header("🌎 Global Overview")
    st.subheader("Global Filters")

    # Create filters
    global_filters = create_filters(
        int(df_merged['YEAR'].min()),
        int(df_merged['YEAR'].max()),
        df_merged,
        "global",
        disease_filter=True,
        region_filter=True,
        top_n_filter=True
    )

    st.markdown("---")

    # Apply filters
    df_global = filter_data(df_merged, global_filters)

    # Get top N countries
    top_countries = df_global.groupby('COUNTRYNAME')['IMMUNISATION_EXPENDITURE'].mean().nlargest(
        global_filters['top_n']).index.tolist()
    df_global_top = df_global[df_global['COUNTRYNAME'].isin(top_countries)]

    # Display metrics
    st.subheader("📈 Global Key Metrics")
    metrics_cols = st.columns(3)
    create_metrics(
        metrics_cols[0], metrics_cols[1], metrics_cols[2],
        "Total Countries", len(df_global['COUNTRYNAME'].unique()),
        "Year Range", f"{global_filters['year_range'][0]} - {global_filters['year_range'][1]}",
        "Total Data Points", len(df_global)
    )

    # Visualizations
    st.subheader("🗺️ Global Immunization Expenditure")
    st.write(f"Showing the top {global_filters['top_n']} countries by average immunization expenditure")

    if len(df_global_top) > 0:
        # Top countries bar chart - interactive
        top_countries_summary = df_global_top.groupby('COUNTRYNAME')['IMMUNISATION_EXPENDITURE'].mean().reset_index()
        top_countries_summary = top_countries_summary.sort_values('IMMUNISATION_EXPENDITURE', ascending=False)

        fig_top = plot_interactive_bar(
            top_countries_summary, 'COUNTRYNAME', 'IMMUNISATION_EXPENDITURE',
            f"Top {global_filters['top_n']} Countries by Average Immunisation Expenditure",
            "Country", "Average Immunisation Expenditure"
        )
        st.plotly_chart(fig_top, use_container_width=True)

        # Global disease cases over time
        st.subheader("📈 Global Disease Cases Over Time")

        # Average trend - interactive
        global_disease_trend = df_global_top.groupby('YEAR')['DISEASE_CASES'].mean().reset_index()
        fig_global_disease = plot_interactive_line(
            global_disease_trend, 'YEAR', 'DISEASE_CASES',
            f"Global Average Disease Cases Over Time (Top {global_filters['top_n']} Countries)",
            "Year", "Average Disease Cases"
        )
        st.plotly_chart(fig_global_disease, use_container_width=True)

        # Individual countries - interactive
        fig_countries = plot_interactive_line(
            df_global_top, 'YEAR', 'DISEASE_CASES',
            "Disease Cases Over Time by Country",
            "Year", "Disease Cases", color='COUNTRYNAME', line_group='COUNTRYNAME'
        )
        st.plotly_chart(fig_countries, use_container_width=True)

        # Correlation analysis - interactive
        st.subheader("🔗 Global Correlation Analysis")
        global_correlations = calculate_correlations(df_global_top)

        fig_global_corr = plot_interactive_bar(
            global_correlations,
            'Country', 'Correlation',
            "Correlation between Immunisation Expenditure and Disease Cases",
            "Country", "Correlation Coefficient"
        )
        st.plotly_chart(fig_global_corr, use_container_width=True)

        # Interpretation
        st.markdown("""
        **Interpretation:**
        - Negative correlation: As immunization expenditure increases, disease cases tend to decrease
        - Positive correlation: Other factors may be influencing the relationship
        """)
    else:
        st.info("No data available for the selected filters.")

st.subheader("📊 Correlation Scatter Plot")
st.write("This scatter plot shows the relationship between immunization expenditure and disease cases")

# Create and display the scatter plot
fig_global_scatter = plot_scatter_with_regression(df_global_top)
st.plotly_chart(fig_global_scatter, use_container_width=True)

# Update the interpretation text
st.markdown("""
**Interpretation:**
- **Negative correlation**: As immunization expenditure increases, disease cases tend to decrease
- **Positive correlation**: Other factors may be influencing the relationship
- **Scatter pattern**: Indicates the strength and consistency of the relationship
- **Outliers**: Points far from the trend line may represent unique situations requiring further investigation
""")

# ASEAN Focus Tab
with asean_tab:
    st.header("🌏 ASEAN Countries Focus")
    st.subheader("ASEAN Filters")

    # Create filters
    asean_filters = create_filters(
        int(df_merged['YEAR'].min()),
        int(df_merged['YEAR'].max()),
        df_merged,
        "asean",
        disease_filter=True
    )

    # ASEAN country selection
    asean_options = [country for country in asean_countries if country in df_merged['COUNTRYNAME'].unique()]
    selected_asean_countries = st.multiselect(
        "Select ASEAN Countries",
        options=asean_options,
        default=asean_options,
        key="asean_country_filter"
    )

    st.markdown("---")

    # Apply filters
    df_asean = filter_data(df_merged, asean_filters, selected_asean_countries)

    # Display metrics
    st.subheader("📈 ASEAN Key Metrics")
    metrics_cols = st.columns(3)
    create_metrics(
        metrics_cols[0], metrics_cols[1], metrics_cols[2],
        "ASEAN Countries", len(df_asean['COUNTRYNAME'].unique()),
        "Year Range", f"{asean_filters['year_range'][0]} - {asean_filters['year_range'][1]}",
        "Total Data Points", len(df_asean)
    )

    # ASEAN visualizations
    st.subheader("🗺️ ASEAN Immunization Expenditure")

    if len(df_asean) > 0:
        # ASEAN countries summary - interactive
        asean_summary = df_asean.groupby('COUNTRYNAME')['IMMUNISATION_EXPENDITURE'].mean().reset_index()
        asean_summary = asean_summary.sort_values('IMMUNISATION_EXPENDITURE', ascending=False)

        fig_asean = plot_interactive_bar(
            asean_summary, 'COUNTRYNAME', 'IMMUNISATION_EXPENDITURE',
            "Average Immunisation Expenditure by ASEAN Country",
            "Country", "Average Immunisation Expenditure"
        )
        st.plotly_chart(fig_asean, use_container_width=True)

        # Disease cases over time - interactive
        fig_asean_disease = plot_interactive_line(
            df_asean, 'YEAR', 'DISEASE_CASES',
            "Disease Cases Over Time in ASEAN Countries",
            "Year", "Disease Cases", color='COUNTRYNAME', line_group='COUNTRYNAME'
        )
        st.plotly_chart(fig_asean_disease, use_container_width=True)

        # Correlation analysis - interactive
        st.subheader("🔗 ASEAN Correlation Analysis")
        asean_correlations = calculate_correlations(df_asean)

        fig_asean_corr = plot_interactive_bar(
            asean_correlations,
            'Country', 'Correlation',
            "Correlation between Immunisation Expenditure and Disease Cases in ASEAN",
            "Country", "Correlation Coefficient"
        )
        st.plotly_chart(fig_asean_corr, use_container_width=True)

        # Interpretation
        st.markdown("""
        **Interpretation:**
        - Negative correlation: As immunization expenditure increases, disease cases tend to decrease
        - Positive correlation: Other factors may be influencing the relationship
        """)
    else:
        st.info("No data available for the selected filters.")

    # Add this code after the correlation bar chart in the ASEAN Focus Tab
    st.subheader("📊 ASEAN Correlation Scatter Plot")
    st.write(
        "This scatter plot shows the relationship between immunization expenditure and disease cases in ASEAN countries")

    # Create and display the scatter plot
    fig_asean_scatter = plot_scatter_with_regression(df_asean)
    st.plotly_chart(fig_asean_scatter, use_container_width=True)

    # Update the interpretation text
    st.markdown("""
    **Interpretation:**
    - **Negative correlation**: As immunization expenditure increases, disease cases tend to decrease
    - **Positive correlation**: Other factors may be influencing the relationship
    - **Country patterns**: Different colors represent different countries, showing how the relationship varies across ASEAN
    - **Trend line**: Shows the overall relationship direction and strength across all selected countries
    """)

    # Create subtabs for ASEAN analyses
    asean_sub_tab1, asean_sub_tab2 = st.tabs(["ASEAN Comparison", "Country Deep Dive"])

    with asean_sub_tab1:
        st.subheader("ASEAN Countries Comparison")

        # Filter spending data
        df_asean_spending = filter_data(df_spending, asean_filters, selected_asean_countries)

        if len(df_asean_spending) > 0:
            # Create tabs for different visualizations
            spend_tab1, spend_tab2 = st.tabs(["Spending Distribution", "Spending Trends"])

            with spend_tab1:
                # Calculate average spending percentages
                asean_spending_summary = df_asean_spending.groupby('COUNTRYNAME')[
                    ['PREVENTIVE_SPENDING_PERCENT', 'TREATMENT_SPENDING_PERCENT']
                ].mean().reset_index()

                # Create interactive stacked bar chart
                fig_spending = go.Figure()

                fig_spending.add_trace(go.Bar(
                    x=asean_spending_summary['COUNTRYNAME'],
                    y=asean_spending_summary['PREVENTIVE_SPENDING_PERCENT'],
                    name='Preventive Spending %',
                    marker_color='green',
                    hovertemplate='%{y:.1f}%<extra>Preventive Spending</extra>'
                ))

                fig_spending.add_trace(go.Bar(
                    x=asean_spending_summary['COUNTRYNAME'],
                    y=asean_spending_summary['TREATMENT_SPENDING_PERCENT'],
                    name='Treatment Spending %',
                    marker_color='blue',
                    hovertemplate='%{y:.1f}%<extra>Treatment Spending</extra>'
                ))

                fig_spending.update_layout(
                    title='Preventive vs Treatment Spending Across ASEAN Countries',
                    xaxis_title='Country',
                    yaxis_title='Spending Percentage',
                    barmode='group',
                    hovermode='closest'
                )

                st.plotly_chart(fig_spending, use_container_width=True)

            with spend_tab2:
                # Create stacked area chart for spending trends over time
                # First, calculate yearly averages across all selected countries
                yearly_spending = df_asean_spending.groupby('YEAR')[
                    ['PREVENTIVE_SPENDING', 'TREATMENT_SPENDING', 'TOTAL_SPENDING']
                ].mean().reset_index()

                # Create the stacked area chart
                fig_area = go.Figure()

                fig_area.add_trace(go.Scatter(
                    x=yearly_spending['YEAR'],
                    y=yearly_spending['PREVENTIVE_SPENDING'],
                    name='Preventive Spending',
                    mode='lines',
                    line=dict(width=0.5, color='green'),
                    stackgroup='one',
                    hovertemplate='Year: %{x}<br>Preventive: %{y:.2f}<extra></extra>'
                ))

                fig_area.add_trace(go.Scatter(
                    x=yearly_spending['YEAR'],
                    y=yearly_spending['TREATMENT_SPENDING'],
                    name='Treatment Spending',
                    mode='lines',
                    line=dict(width=0.5, color='blue'),
                    stackgroup='one',
                    hovertemplate='Year: %{x}<br>Treatment: %{y:.2f}<extra></extra>'
                ))

                fig_area.update_layout(
                    title='ASEAN Spending Trends Over Time (Average across selected countries)',
                    xaxis_title='Year',
                    yaxis_title='Average Spending',
                    hovermode='closest',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )

                st.plotly_chart(fig_area, use_container_width=True)



    with asean_sub_tab2:
        st.subheader("Individual Country Deep Dive")

        # Country selector
        selected_country = st.selectbox(
            "Select ASEAN Country for Deep Dive",
            options=selected_asean_countries if selected_asean_countries else asean_options,
            key="country_deep_dive"
        )

        # Filter for selected country
        df_country = df_asean[df_asean['COUNTRYNAME'] == selected_country].sort_values('YEAR')
        df_country_spending = df_asean_spending[df_asean_spending['COUNTRYNAME'] == selected_country].sort_values(
            'YEAR')

        if len(df_country) > 0:
            # Create tabs for different views
            country_tab1, country_tab2 = st.tabs(["Trend Analysis", "COVID-19 Impact Analysis"])

            with country_tab1:
                # Interactive dual-axis chart
                fig_country = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=(
                        f'{selected_country}: Immunisation Expenditure vs Disease Cases',
                        f'{selected_country}: Preventive vs Treatment Spending Over Years'
                    ),
                    specs=[[{"secondary_y": True}], [{"secondary_y": False}]],
                    vertical_spacing=0.12
                )

                # Top chart - Expenditure and cases
                fig_country.add_trace(
                    go.Scatter(
                        x=df_country['YEAR'],
                        y=df_country['IMMUNISATION_EXPENDITURE'],
                        name='Immunisation Expenditure',
                        line=dict(color='blue', width=3),
                        mode='lines+markers',
                        hovertemplate='Year: %{x}<br>Expenditure: %{y:.2f}<extra></extra>'
                    ),
                    row=1, col=1
                )

                fig_country.add_trace(
                    go.Scatter(
                        x=df_country['YEAR'],
                        y=df_country['DISEASE_CASES'],
                        name='Disease Cases',
                        line=dict(color='red', width=3),
                        mode='lines+markers',
                        hovertemplate='Year: %{x}<br>Cases: %{y:.2f}<extra></extra>'
                    ),
                    row=1, col=1, secondary_y=True
                )

                # Bottom chart - Spending percentages
                if len(df_country_spending) > 0:
                    fig_country.add_trace(
                        go.Bar(
                            x=df_country_spending['YEAR'],
                            y=df_country_spending['PREVENTIVE_SPENDING_PERCENT'],
                            name='Preventive Spending %',
                            marker_color='green',
                            hovertemplate='Year: %{x}<br>Preventive: %{y:.1f}%<extra></extra>'
                        ),
                        row=2, col=1
                    )

                    fig_country.add_trace(
                        go.Bar(
                            x=df_country_spending['YEAR'],
                            y=df_country_spending['TREATMENT_SPENDING_PERCENT'],
                            name='Treatment Spending %',
                            marker_color='blue',
                            hovertemplate='Year: %{x}<br>Treatment: %{y:.1f}%<extra></extra>'
                        ),
                        row=2, col=1
                    )

                    fig_country.update_layout(barmode='group')

                # Update layout and axes
                fig_country.update_layout(
                    height=800,
                    hovermode='closest',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )

                # Update axes labels
                fig_country.update_xaxes(title_text="Year", row=1, col=1)
                fig_country.update_xaxes(title_text="Year", row=2, col=1)
                fig_country.update_yaxes(title_text="Immunisation Expenditure", row=1, col=1)
                fig_country.update_yaxes(title_text="Disease Cases", secondary_y=True, row=1, col=1)
                fig_country.update_yaxes(title_text="Spending Percentage", row=2, col=1)

                st.plotly_chart(fig_country, use_container_width=True)

                # Scatter plot for this country
                st.subheader("Correlation Analysis")
                fig_country_scatter = plot_scatter_with_regression(df_country, selected_country)
                st.plotly_chart(fig_country_scatter, use_container_width=True)

            with country_tab2:
                st.subheader("COVID-19 Impact Analysis (2019-2021)")

                # Filter for pre and post COVID periods
                pre_covid = df_country[df_country['YEAR'] == 2019] if 2019 in df_country[
                    'YEAR'].values else pd.DataFrame()
                during_covid = df_country[df_country['YEAR'].isin([2020, 2021])]

                if not pre_covid.empty and not during_covid.empty:
                    # Calculate yearly changes
                    df_yearly_change = df_country.copy()
                    df_yearly_change['EXPENDITURE_PCT_CHANGE'] = df_yearly_change[
                                                                     'IMMUNISATION_EXPENDITURE'].pct_change() * 100
                    df_yearly_change['CASES_PCT_CHANGE'] = df_yearly_change['DISEASE_CASES'].pct_change() * 100

                    # Create the yearly change chart
                    fig_yearly_change = make_subplots(
                        rows=1, cols=2,
                        subplot_titles=(
                            f'Yearly % Change in Expenditure',
                            f'Yearly % Change in Disease Cases'
                        ),
                        specs=[[{"type": "bar"}, {"type": "bar"}]],
                        horizontal_spacing=0.1
                    )

                    # Expenditure changes
                    fig_yearly_change.add_trace(
                        go.Bar(
                            x=df_yearly_change['YEAR'][1:],  # Skip first year as it has no change
                            y=df_yearly_change['EXPENDITURE_PCT_CHANGE'][1:],
                            name='% Change in Expenditure',
                            marker_color=['green' if x >= 0 else 'red' for x in
                                          df_yearly_change['EXPENDITURE_PCT_CHANGE'][1:]],
                            hovertemplate='Year: %{x}<br>Change: %{y:.1f}%<extra></extra>'
                        ),
                        row=1, col=1
                    )

                    # Disease case changes
                    fig_yearly_change.add_trace(
                        go.Bar(
                            x=df_yearly_change['YEAR'][1:],  # Skip first year as it has no change
                            y=df_yearly_change['CASES_PCT_CHANGE'][1:],
                            name='% Change in Cases',
                            marker_color=['red' if x >= 0 else 'green' for x in
                                          df_yearly_change['CASES_PCT_CHANGE'][1:]],
                            hovertemplate='Year: %{x}<br>Change: %{y:.1f}%<extra></extra>'
                        ),
                        row=1, col=2
                    )

                    # Update layout
                    fig_yearly_change.update_layout(
                        height=500,
                        title_text=f"Yearly Percentage Changes for {selected_country} (2019-2021)",
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )

                    # Update axes
                    fig_yearly_change.update_yaxes(title_text="% Change", row=1, col=1)
                    fig_yearly_change.update_yaxes(title_text="% Change", row=1, col=2)

                    st.plotly_chart(fig_yearly_change, use_container_width=True)

                    # Pre-COVID vs. During COVID comparison
                    st.subheader("Pre-COVID vs. During COVID Comparison")

                    # Calculate averages
                    pre_covid_exp = pre_covid['IMMUNISATION_EXPENDITURE'].mean()
                    pre_covid_cases = pre_covid['DISEASE_CASES'].mean()
                    during_covid_exp = during_covid['IMMUNISATION_EXPENDITURE'].mean()
                    during_covid_cases = during_covid['DISEASE_CASES'].mean()

                    # Calculate percentage changes
                    exp_change = ((during_covid_exp - pre_covid_exp) / pre_covid_exp) * 100
                    cases_change = ((during_covid_cases - pre_covid_cases) / pre_covid_cases) * 100

                    # Determine trends
                    exp_trend = "Increased" if exp_change > 0 else "Decreased"
                    cases_trend = "Increased" if cases_change > 0 else "Decreased"

                    # Color indicators
                    exp_color = "green" if exp_change > 0 else "red"
                    cases_color = "red" if cases_change > 0 else "green"

                    # Create columns for metrics
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"### Immunization Expenditure")
                        st.markdown(f"**Pre-COVID (2019):** {format_number(pre_covid_exp)}")
                        st.markdown(f"**During COVID (2020-2021):** {format_number(during_covid_exp)}")
                        st.markdown(
                            f"**Change:** <span style='color:{exp_color}'>{exp_change:.1f}% ({exp_trend})</span>",
                            unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"### Disease Cases")
                        st.markdown(f"**Pre-COVID (2019):** {format_number(pre_covid_cases)}")
                        st.markdown(f"**During COVID (2020-2021):** {format_number(during_covid_cases)}")
                        st.markdown(
                            f"**Change:** <span style='color:{cases_color}'>{cases_change:.1f}% ({cases_trend})</span>",
                            unsafe_allow_html=True)

                    # Calculate ROI and Cost-Effectiveness metrics
                    st.markdown("---")
                    st.subheader("Investment Analysis")

                    # 1. Calculate absolute change in cases and expenditure
                    absolute_case_change = pre_covid_cases - during_covid_cases
                    absolute_exp_change = during_covid_exp - pre_covid_exp

                    # 2. Cost per Case Reduction (Cost-Effectiveness)
                    if cases_change < 0:  # Only calculate if cases decreased
                        cost_per_case_reduction = absolute_exp_change / absolute_case_change
                        cost_effectiveness_color = "green" if cost_per_case_reduction < pre_covid_exp else "orange"
                    else:
                        cost_per_case_reduction = 0
                        cost_effectiveness_color = "red"

                    # 3. Return on Investment (ROI)
                    # Assuming each disease case has an estimated economic cost (can be adjusted based on country)
                    estimated_cost_per_case = 5000  # Default value in currency units (adjust as needed for your context)

                    # Calculate economic benefit from case reduction
                    economic_benefit = absolute_case_change * estimated_cost_per_case
                    roi = ((
                                       economic_benefit - absolute_exp_change) / absolute_exp_change) * 100 if absolute_exp_change > 0 else 0
                    roi_color = "green" if roi > 0 else "red"

                    # 4. Optimal Investment Projection
                    # Using a simple linear model to estimate optimal investment
                    if cases_change < 0 and exp_change > 0:
                        # Calculate the effectiveness ratio (how much % reduction in cases per % increase in spending)
                        effectiveness_ratio = abs(cases_change) / exp_change

                        # Project what would happen with different investment levels
                        investment_scenarios = {
                            "current": during_covid_exp,
                            "increase_10": during_covid_exp * 1.1,
                            "increase_25": during_covid_exp * 1.25,
                            "increase_50": during_covid_exp * 1.5
                        }

                        # Calculate projected case reductions
                        case_projections = {}
                        for scenario, investment in investment_scenarios.items():
                            if scenario == "current":
                                case_projections[scenario] = during_covid_cases
                            else:
                                # Calculate percent increase in investment from current
                                percent_increase = ((investment - during_covid_exp) / during_covid_exp) * 100
                                # Estimate percent decrease in cases using the effectiveness ratio
                                projected_percent_decrease = percent_increase * effectiveness_ratio
                                # Calculate projected cases
                                projected_cases = during_covid_cases * (1 - (projected_percent_decrease / 100))
                                case_projections[scenario] = max(0, projected_cases)  # Ensure no negative cases

                    # Create ROI and Cost-Effectiveness display
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### Cost-Effectiveness Analysis")
                        if cases_change < 0:
                            st.markdown(
                                f"**Cost per Case Reduced:** <span style='color:{cost_effectiveness_color}'>{format_number(cost_per_case_reduction)}</span>",
                                unsafe_allow_html=True)
                            st.markdown(
                                f"**Effectiveness Ratio:** {effectiveness_ratio:.2f}% reduction in cases per 1% increase in spending")
                        else:
                            st.markdown("**Cost-Effectiveness:** Cannot calculate (cases increased)")

                    with col2:
                        st.markdown("### Return on Investment (ROI)")
                        st.markdown(f"**Estimated Economic Benefit:** {format_number(economic_benefit)}")
                        st.markdown(f"**ROI:** <span style='color:{roi_color}'>{roi:.2f}%</span>",
                                    unsafe_allow_html=True)
                        st.markdown(
                            f"*Based on estimated cost per disease case of {format_number(estimated_cost_per_case)}*")

                    # Create insight summary box
                    st.markdown("---")
                    st.subheader("Insight Summary")

                    # Determine overall health indicator
                    if cases_change <= 0:
                        health_indicator = "green"
                        health_status = "Improving"
                    else:
                        health_indicator = "red"
                        health_status = "Declining"

                    # Create styled box
                    st.markdown(f"""
                    <div style="
                        border: 2px solid {health_indicator};
                        border-radius: 10px;
                        padding: 20px;
                        background-color: rgba({0 if health_indicator == 'green' else 255}, {255 if health_indicator == 'green' else 0}, 0, 0.1);
                        margin-bottom: 20px;
                    ">
                        <h3 style="color: {health_indicator};">Health Status: {health_status}</h3>
                        <p><strong>Expenditure Trend:</strong> {exp_trend} by {abs(exp_change):.1f}%</p>
                        <p><strong>Disease Cases Trend:</strong> {cases_trend} by {abs(cases_change):.1f}%</p>
                        <p><strong>Cost-Effectiveness:</strong> {format_number(cost_per_case_reduction)} per case reduced</p>
                        <p><strong>Return on Investment:</strong> {roi:.2f}%</p>
                        <p><strong>Impact Summary:</strong> During the COVID-19 period (2020-2021), {selected_country} 
                        {f"increased immunization expenditure while disease cases decreased, indicating effective healthcare intervention."
                    if exp_change > 0 and cases_change < 0 else
                    f"decreased immunization expenditure while disease cases increased, suggesting possible healthcare system strain."
                    if exp_change < 0 and cases_change > 0 else
                    f"increased immunization expenditure but disease cases also increased, suggesting complex factors beyond expenditure alone."
                    if exp_change > 0 and cases_change > 0 else
                    f"decreased immunization expenditure and disease cases also decreased, suggesting possible efficiency improvements or reporting changes."}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Investment Recommendation
                    st.markdown("---")
                    st.subheader("Investment Recommendation")

                    # Create a recommendation box
                    if cases_change < 0 and exp_change > 0:
                        recommendation_color = "green"

                        # Find the optimal investment scenario (highest ROI)
                        optimal_increase = 0
                        for increase in [10, 25, 50]:
                            scenario_investment = during_covid_exp * (1 + increase / 100)
                            scenario_case_reduction = during_covid_cases * (effectiveness_ratio * increase / 100)
                            scenario_benefit = scenario_case_reduction * estimated_cost_per_case
                            scenario_roi = ((scenario_benefit - (scenario_investment - during_covid_exp)) / (
                                    scenario_investment - during_covid_exp)) * 100

                            if scenario_roi > roi:
                                optimal_increase = increase
                                roi = scenario_roi

                        if optimal_increase > 0:
                            recommendation = f"Increase immunization expenditure by approximately {optimal_increase}% for optimal returns"
                        else:
                            recommendation = "Maintain current immunization expenditure levels which show positive returns"

                    elif exp_change > 0 and cases_change > 0:
                        recommendation_color = "orange"
                        recommendation = "Review immunization strategy - despite increased spending, cases have risen"
                    elif exp_change < 0 and cases_change < 0:
                        recommendation_color = "blue"
                        recommendation = "Investigate efficiency improvements that allowed for case reduction despite decreased spending"
                    else:
                        recommendation_color = "red"
                        recommendation = "Urgently increase immunization expenditure to address rising disease cases"

                    # Create styled recommendation box
                    st.markdown(f"""
                    <div style="
                        border: 2px solid {recommendation_color};
                        border-radius: 10px;
                        padding: 20px;
                        background-color: rgba({0 if recommendation_color == 'green' else 255},
                                                {255 if recommendation_color in ['green', 'blue'] else 165 if recommendation_color == 'orange' else 0},
                                                {255 if recommendation_color == 'blue' else 0}, 0.1);
                        margin-bottom: 20px;
                    ">
                        <h3>Recommended Action:</h3>
                        <p style="font-size: 18px;">{recommendation}</p>
                        <p><strong>Investment-to-Outcome Analysis:</strong> For every 1% increase in immunization expenditure, 
                        a {effectiveness_ratio:.2f}% reduction in disease cases can be expected based on historical data.</p>
                        <p><strong>Projected Outcomes with Additional Investment:</strong></p>
                        <ul>
                            <li>Current spending ({format_number(during_covid_exp)}): {format_number(during_covid_cases)} cases</li>
                            <li>+10% spending ({format_number(investment_scenarios['increase_10'])}): {format_number(case_projections['increase_10'])} cases</li>
                            <li>+25% spending ({format_number(investment_scenarios['increase_25'])}): {format_number(case_projections['increase_25'])} cases</li>
                            <li>+50% spending ({format_number(investment_scenarios['increase_50'])}): {format_number(case_projections['increase_50'])} cases</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

            # Key insights section shown below both tabs
            st.markdown("---")
            st.subheader(f"Key Metrics for {selected_country}")

            # Calculate metrics
            avg_expenditure = df_country['IMMUNISATION_EXPENDITURE'].mean()
            avg_cases = df_country['DISEASE_CASES'].mean()
            correlation = df_country['IMMUNISATION_EXPENDITURE'].corr(df_country['DISEASE_CASES'])

            # Display metrics
            key_metrics_cols = st.columns(3)
            with key_metrics_cols[0]:
                st.metric(label="Average Immunisation Expenditure",
                          value=f"{avg_expenditure:.2f}")

            with key_metrics_cols[1]:
                st.metric(label="Average Disease Cases",
                          value=f"{avg_cases:.2f}")

            with key_metrics_cols[2]:
                st.metric(label="Correlation Coefficient",
                          value=f"{correlation:.2f}")
        else:
            st.info(f"No data available for {selected_country}.")

# Data Preview
st.subheader("📊 Data Preview")
st.dataframe(df_merged.head(10), use_container_width=True)

# Download button
csv = df_merged.to_csv(index=False)
st.download_button(
    label="Download Full Data as CSV",
    data=csv,
    file_name="immunization_disease_data.csv",
    mime="text/csv",
)

# Metadata
with st.expander("📋 Data Source Information"):
    st.write("""
    **Data Sources:**
    - **[Immunization Expenditure](https://immunizationdata.who.int/global/wiise-detail-page/immunization-expenditure?ISO_3_CODE=&YEAR=)** : Expenditure on vaccination programs
    - **[Infectious Disease](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/uhc-sci-components-infectious-diseases)** : Number of cases reported

    **Analysis Notes:**
    - Data has been filtered to show only records with both immunization expenditure and disease cases
    - The analysis explores the relationship between government spending on immunization and disease prevalence
    - ASEAN countries analysis is included to provide regional insights
    """)

# Add requirements note
with st.expander("📦 Package Requirements"):
    st.code("""
    # Required packages
    streamlit
    pandas
    matplotlib
    seaborn
    numpy
    plotly
    """)
