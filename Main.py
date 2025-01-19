import streamlit as st
import pandas as pd
import os
from PIL import Image

# Configuración inicial
st.set_page_config(page_title="Padel Crack", layout="wide")
st.title("\ud83c\udfbe Padel Crack")
st.sidebar.title("Menú Principal")

# Archivos CSV
USERS_CSV = "usuarios.csv"
ADMINS_CSV = "admins.csv"

def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

def save_data(data, file_path):
    data.to_csv(file_path, index=False)

def user_registration():
    st.subheader("Registro de Usuario")
    with st.form("registro_usuario"):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        edad = st.number_input("Edad", min_value=0, max_value=100, step=1)
        email = st.text_input("Email")
        nacionalidad = st.text_input("Nacionalidad")
        zona_principal = st.text_input("Zona principal donde juega")
        zona_secundaria = st.text_input("Zona secundaria donde juega")
        submit_button = st.form_submit_button("Registrar")

        if submit_button:
            if not nombre or not apellido or not email:
                st.error("Por favor, completa todos los campos obligatorios.")
                return

            users = load_data(USERS_CSV)

            if not users.empty and email in users["Email"].values:
                st.error("Ese usuario ya existe.")
            else:
                user_id = f"USR{len(users) + 1:04d}"
                nuevo_usuario = {
                    "UsuarioID": user_id,
                    "Nombre": nombre,
                    "Apellido": apellido,
                    "Edad": edad,
                    "Email": email,
                    "Nacionalidad": nacionalidad,
                    "Zona_Principal": zona_principal,
                    "Zona_Secundaria": zona_secundaria,
                }
                users = users.append(nuevo_usuario, ignore_index=True)
                save_data(users, USERS_CSV)
                st.success(f"Usuario registrado con éxito. ID: {user_id}")

def admin_registration():
    st.subheader("Registro de Administrador")
    with st.form("registro_admin"):
        nombre_club = st.text_input("Nombre del club o cancha")
        lugar = st.text_input("Lugar")
        horarios = st.text_input("Horarios y días de atención")
        fotos = st.file_uploader("Fotos del lugar (máximo 5)", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
        submit_button = st.form_submit_button("Registrar")

        if submit_button:
            if not nombre_club or not lugar or not horarios:
                st.error("Por favor, completa todos los campos obligatorios.")
                return

            admins = load_data(ADMINS_CSV)

            admin_id = f"ADM{len(admins) + 1:04d}"
            nuevo_admin = {
                "AdminID": admin_id,
                "Nombre_Club": nombre_club,
                "Lugar": lugar,
                "Horarios": horarios,
            }
            admins = admins.append(nuevo_admin, ignore_index=True)
            save_data(admins, ADMINS_CSV)
            st.success(f"Administrador registrado con éxito. ID: {admin_id}")

# Navegación
menu = st.sidebar.radio("Selecciona una opción", ["Inicio", "Registro Usuario", "Registro Admin", "Acceso Usuario", "Acceso Admin"])

if menu == "Inicio":
    st.header("Bienvenido a Padel Crack \ud83c\udfbe")
    st.write("Una plataforma creada para conectar jugadores, clubes y entrenadores de padel.")

elif menu == "Registro Usuario":
    user_registration()

elif menu == "Registro Admin":
    admin_registration()

elif menu == "Acceso Usuario":
    st.subheader("Acceso de Usuario")
    user_id = st.text_input("Ingresa tu UsuarioID")
    users = load_data(USERS_CSV)

    if st.button("Entrar"):
        if user_id in users["UsuarioID"].values:
            st.success(f"Bienvenido, {users[users['UsuarioID'] == user_id]['Nombre'].values[0]}!")
            # Aquí iría el menú del usuario
        else:
            st.error("UsuarioID no encontrado.")

elif menu == "Acceso Admin":
    st.subheader("Acceso de Administrador")
    admin_id = st.text_input("Ingresa tu AdminID")
    admins = load_data(ADMINS_CSV)

    if st.button("Entrar"):
        if admin_id in admins["AdminID"].values:
            st.success(f"Bienvenido, {admins[admins['AdminID'] == admin_id]['Nombre_Club'].values[0]}!")
            # Aquí iría el menú del administrador
        else:
            st.error("AdminID no encontrado.")

