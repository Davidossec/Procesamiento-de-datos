import streamlit as st
import pandas as pd
import plotly.express as px

# Función para cargar el archivo
def cargar_archivo():
    uploaded_file = st.file_uploader("Cargar archivo", type=["csv", "xlsx"])
    return uploaded_file

# Función para leer los datos del archivo cargado
def leer_datos(uploaded_file):
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    return df

# Función para mostrar las primeras filas del DataFrame
def mostrar_primeras_filas(df):
    st.write("Primeras filas del DataFrame:")
    st.write(df.head(10))

# Función para mostrar los tipos de datos del DataFrame
def mostrar_tipos_de_datos(df):
    st.write("Tipo de datos que encontramos:")
    st.write(df.dtypes)

# Función para mostrar los datos únicos del DataFrame
def mostrar_datos_unicos(df):
    st.write("Datos únicos:")
    st.write(df.nunique())

# Función para verificar si hay valores duplicados en el DataFrame
def verificar_duplicados(df):
    if df.duplicated().any():
        st.write('Sí, hay valores duplicados:', df.duplicated().sum())
    else:
        st.write('No hay valores duplicados')

# Función para mostrar un gráfico de valores faltantes por columna
def grafico_valores_faltantes(df):
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    fig = px.bar(x=missing_percentage.index, y=missing_percentage.values, labels={"x": "Columna", "y": "Porcentaje"})
    fig.update_layout(title="Porcentaje de Valores Faltantes por Columna", xaxis_title="", yaxis_title="Porcentaje")
    st.plotly_chart(fig)

# Función para eliminar los valores duplicados del DataFrame
def eliminar_duplicados():
    if 'df' in st.session_state:
        df_sin_duplicados = st.session_state.df.drop_duplicates()
        st.session_state.df = df_sin_duplicados
        st.write("¡DataFrame sin duplicados!:")
        st.write(df_sin_duplicados)
    else:
        st.write("No se ha cargado un DataFrame.")

# Función para manejar los valores faltantes en el DataFrame
def manejar_valores_faltantes(thresh):
    if 'df' in st.session_state:
        df = st.session_state.df
        columnas_a_eliminar = df.columns[df.isnull().sum() / len(df) * 100 > thresh]
        df_sin_columnas_faltantes = df.drop(columns=columnas_a_eliminar)
        st.session_state.df = df_sin_columnas_faltantes
        st.write("DataFrame sin columnas faltantes:")
        st.write(df_sin_columnas_faltantes)
    else:
        st.write("No se ha cargado un DataFrame.")

# Función para guardar el DataFrame original en session state
def guardar_dataframe_original(df):
    if 'original_df' not in st.session_state:
        st.session_state['original_df'] = df.copy()

# Función para volver al DataFrame original
def volver_dataframe_original():
    if st.button("Volver al dataframe original"):
        if 'original_df' in st.session_state:
            st.session_state.df = st.session_state['original_df'].copy()
            st.write("DataFrame original restaurado:")
            st.write(st.session_state.df)
        else:
            st.write("No se ha cargado un DataFrame original.")

# Función para guardar el DataFrame modificado
def guardar():
    if st.button("Guardar"):
        if 'df' in st.session_state:
            st.write("Variable guardada")
            # Código para guardar el DataFrame
        else:
            st.write("No se ha cargado un DataFrame.")

# Función para el botón de eliminar duplicados
def boton_eliminar_duplicados():
    if st.button("Eliminar Duplicados"):
        eliminar_duplicados()

# Función para el slider de umbral de valores faltantes
def slider_valores_faltantes():
    thresh = st.slider("Selecciona el umbral de valores faltantes(%)", min_value=0, max_value=100, value=10)
    manejar_valores_faltantes(thresh)

# Función principal que llama a las demás funciones
def main():
    st.title("Visualización de Valores Faltantes")
    uploaded_file = cargar_archivo()
    if uploaded_file is not None:
        df = leer_datos(uploaded_file)
        st.session_state.df = df  # Guardar el DataFrame en session state
        guardar_dataframe_original(df)  # Guardar el DataFrame original en session state

        volver_dataframe_original()  # Botón para volver al DataFrame original
        mostrar_primeras_filas(df)
        mostrar_tipos_de_datos(df)
        mostrar_datos_unicos(df)
        verificar_duplicados(df)
        grafico_valores_faltantes(df)
        
        boton_eliminar_duplicados()
        slider_valores_faltantes()
        guardar()

if __name__ == "__main__":
    main()

