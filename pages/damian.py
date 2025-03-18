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
st.markdown(
    "This dashboard analyzes the relationship between immunization expenditures and infectious disease cases across different countries over time.")


# Define helper functions
def create_metrics(col1, col2, col3, metric1, value1, metric2, value2, metric3, value3):
    with col1:
        st.metric(metric1, value1)
    with col2:
        st.metric(metric2, value2)
    with col3:
        st.metric(metric3, value3)


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

    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        hovermode="closest"
    )

    # Add zoom and pan buttons
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=[
                    dict(
                        args=[{"yaxis.autorange": True, "xaxis.autorange": True}],
                        label="Reset Zoom",
                        method="relayout"
                    )
                ],
                pad={"r": 10, "t": 10},
                showactive=False,
                x=0.11,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
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
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        hovermode="closest"
    )

    # Add zoom and pan buttons
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=[
                    dict(
                        args=[{"yaxis.autorange": True, "xaxis.autorange": True}],
                        label="Reset Zoom",
                        method="relayout"
                    )
                ],
                pad={"r": 10, "t": 10},
                showactive=False,
                x=0.11,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    return fig


def calculate_correlations(df, group_by='COUNTRYNAME'):
    corr_df = df.groupby(group_by).apply(
        lambda x: x['IMMUNISATION_EXPENDITURE'].corr(x['DISEASE_CASES'])
    ).reset_index()
    corr_df.columns = ['Country', 'Correlation']
    return corr_df.sort_values('Correlation')


@st.cache_data
def load_data():
    # Replace with your actual file paths
    file1 = "data\Immunization_expenditure.csv"
    file2 = "data\Infectious_Disease.csv"

    df_immunization = pd.read_csv(file1, encoding='ISO-8859-1')
    df_disease = pd.read_csv(file2')
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
    create_metrics(
        st.columns(3)[0], st.columns(3)[1], st.columns(3)[2],
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
    create_metrics(
        st.columns(3)[0], st.columns(3)[1], st.columns(3)[2],
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

    # Create subtabs for ASEAN analyses
    asean_sub_tab1, asean_sub_tab2 = st.tabs(["ASEAN Comparison", "Country Deep Dive"])

    with asean_sub_tab1:
        st.subheader("ASEAN Countries Comparison")

        # Filter spending data
        df_asean_spending = filter_data(df_spending, asean_filters, selected_asean_countries)

        if len(df_asean_spending) > 0:
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

            # Add zoom and pan buttons
            fig_spending.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="left",
                        buttons=[
                            dict(
                                args=[{"yaxis.autorange": True, "xaxis.autorange": True}],
                                label="Reset Zoom",
                                method="relayout"
                            )
                        ],
                        pad={"r": 10, "t": 10},
                        showactive=False,
                        x=0.11,
                        xanchor="left",
                        y=1.1,
                        yanchor="top"
                    ),
                ]
            )

            st.plotly_chart(fig_spending, use_container_width=True)
        else:
            st.info("No spending data available for the selected filters.")

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

            # Add zoom and pan buttons
            fig_country.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="left",
                        buttons=[
                            dict(
                                args=[{"yaxis.autorange": True, "xaxis.autorange": True,
                                       "yaxis2.autorange": True, "yaxis3.autorange": True,
                                       "xaxis2.autorange": True}],
                                label="Reset Zoom",
                                method="relayout"
                            )
                        ],
                        pad={"r": 10, "t": 10},
                        showactive=False,
                        x=0.11,
                        xanchor="left",
                        y=1.1,
                        yanchor="top"
                    ),
                ]
            )

            st.plotly_chart(fig_country, use_container_width=True)

            # Key insights
            st.subheader(f"Key Insights for {selected_country}")

            # Calculate metrics
            avg_expenditure = df_country['IMMUNISATION_EXPENDITURE'].mean()
            avg_cases = df_country['DISEASE_CASES'].mean()
            correlation = df_country['IMMUNISATION_EXPENDITURE'].corr(df_country['DISEASE_CASES'])

            # Display metrics
            create_metrics(
                st.columns(3)[0], st.columns(3)[1], st.columns(3)[2],
                "Average Immunisation Expenditure", f"{avg_expenditure:.2f}",
                "Average Disease Cases", f"{avg_cases:.2f}",
                "Correlation", f"{correlation:.2f}"
            )

            # Interpretation
            correlation_text = "negative" if correlation < 0 else "positive"
            interpretation = f"This {correlation_text} correlation suggests that " + (
                "higher immunization expenditure is associated with lower disease cases." if correlation < 0 else
                "other factors may be influencing the relationship between immunization expenditure and disease cases."
            )

            st.markdown(f"""
            **Interpretation for {selected_country}:**
            - The correlation between immunization expenditure and disease cases is {correlation:.2f}
            - {interpretation}
            """)
        else:
            st.info(f"No data available for {selected_country}.")

# Data Preview
st.subheader("📊 Data Preview")
st.dataframe(df_merged.head(10), use_container_width=True)

# Add interactive data table
st.subheader("🔍 Interactive Data Explorer")
st.write("Use the search box and sorting features to explore the data")

# Convert to interactive table with plotly
fig_table = go.Figure(data=[go.Table(
    header=dict(
        values=list(df_merged.columns),
        fill_color='royalblue',
        align='left',
        font=dict(color='white', size=12)
    ),
    cells=dict(
        values=[df_merged[col] for col in df_merged.columns],
        fill_color='lavender',
        align='left'
    )
)])

fig_table.update_layout(
    height=500,
    title="Full Dataset Preview (First 100 rows)"
)

st.plotly_chart(fig_table, use_container_width=True)

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
    - Immunization Expenditure: Expenditure on vaccination programs
    - Infectious Disease: Number of cases reported

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
