import streamlit as st
import pandas as pd
from analysis import DataAnalyzer
import io

# Configure the app
st.set_page_config(page_title="Universal Data Analysis Tool", layout="wide")
st.title("📊 Universal Data Analysis Tool (Excel/CSV)")

# Sidebar for user inputs
with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader("Upload Excel/CSV", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Load data
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        analyzer = DataAnalyzer(df)
        all_columns = df.columns.tolist()
        numeric_columns = df.select_dtypes(include='number').columns.tolist()

        st.sidebar.markdown("---")
        st.sidebar.write("### Column Selection")
        selected_columns = st.sidebar.multiselect(
            "Select columns to analyze (numeric columns recommended)",
            options=numeric_columns,
            default=numeric_columns
        )

        st.sidebar.write("### Row Selection for Comparison")
        row_indices = st.sidebar.multiselect(
            "Select row indices for comparison (by index)",
            options=list(df.index),
            default=list(df.index)[:2]
        )

        st.sidebar.write("### Visualization Options")
        chart_types = st.sidebar.multiselect(
            "Select chart types to display",
            ["Bar Chart", "Line Chart", "Box Plot"],
            default=["Bar Chart"]
        )
        chart_width = st.sidebar.slider("Chart width (px)", 300, 1200, 600, 50)
        chart_height = st.sidebar.slider("Chart height (px)", 200, 1000, 400, 50)

        # Display data preview with filtering
        st.subheader("Data Preview (with Filter)")
        filter_col = st.selectbox("Filter by column (optional)", ["None"] + all_columns)
        if filter_col != "None":
            unique_vals = df[filter_col].unique()
            filter_val = st.selectbox(f"Select value in '{filter_col}'", unique_vals)
            df_filtered = df[df[filter_col] == filter_val]
        else:
            df_filtered = df
        st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

        # Show statistics
        st.subheader("Statistics (Selected Columns)")
        stats = analyzer.get_statistics(selected_columns)
        # Conditional formatting: highlight max/min
        styled_stats = stats.style.highlight_max(axis=1, color='lightgreen').highlight_min(axis=1, color='lightcoral')
        st.dataframe(styled_stats, use_container_width=True)
        # Export statistics
        stats_csv = stats.to_csv().encode('utf-8')
        st.download_button("Download Statistics as CSV", stats_csv, "statistics.csv", "text/csv")
        stats_excel = io.BytesIO()
        stats.to_excel(stats_excel)
        st.download_button("Download Statistics as Excel", stats_excel.getvalue(), "statistics.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # Show summary/insights
        st.subheader("Summary Insights")
        for col in selected_columns:
            col_data = df[col].dropna()
            if not col_data.empty:
                st.markdown(f"**{col}:** Mean = {col_data.mean():.2f}, Median = {col_data.median():.2f}, Min = {col_data.min()}, Max = {col_data.max()}, Std = {col_data.std():.2f}")

        # Show comparison between selected rows
        st.subheader("Comparison Between Selected Rows (Selected Columns)")
        if row_indices and selected_columns:
            comparison_df = analyzer.compare_rows(row_indices, selected_columns)
            # Conditional formatting: highlight max/min per column
            styled_comp = comparison_df.style.highlight_max(axis=0, color='lightgreen').highlight_min(axis=0, color='lightcoral')
            st.dataframe(styled_comp, use_container_width=True)
            # Export comparison
            comp_csv = comparison_df.to_csv().encode('utf-8')
            st.download_button("Download Comparison as CSV", comp_csv, "comparison.csv", "text/csv")
            comp_excel = io.BytesIO()
            comparison_df.to_excel(comp_excel)
            st.download_button("Download Comparison as Excel", comp_excel.getvalue(), "comparison.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.info("Select at least one row and one column for comparison.")

        # Show multiple charts in a row
        st.subheader("Visualization")
        chart_cols = st.columns(len(chart_types)) if chart_types else []
        import matplotlib.pyplot as plt
        for i, chart_type in enumerate(chart_types):
            with chart_cols[i]:
                fig = None
                if chart_type == "Bar Chart" and row_indices and selected_columns:
                    fig = analyzer.plot_bar(row_indices, selected_columns)
                elif chart_type == "Line Chart" and row_indices and selected_columns:
                    fig = analyzer.plot_line(row_indices, selected_columns)
                elif chart_type == "Box Plot" and selected_columns:
                    fig = analyzer.plot_box(selected_columns)
                if fig is not None:
                    fig.set_size_inches(chart_width/100, chart_height/100)
                    st.pyplot(fig)
                    plot_buffer = io.BytesIO()
                    fig.savefig(plot_buffer, format='png')
                    st.download_button(f"Download {chart_type} as PNG", plot_buffer.getvalue(), f"{chart_type.lower().replace(' ', '_')}.png", "image/png")
                else:
                    st.info(f"Select appropriate data for {chart_type}.")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.warning("Please upload a file to begin.")
