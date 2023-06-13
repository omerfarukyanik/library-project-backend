ADMIN_LOGIN_SQL = """SELECT * FROM 
public.admin WHERE admin_user_name='{0}';"""
USER_LOGIN_SQL = """SELECT * FROM 
public.customer WHERE user_name='{0}';"""
ADMIN_SIGN_UP_SQL = """INSERT INTO public.admin(admin_user_name, password, email, first_name, last_name, 
profile_picture_path) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');"""
USER_SIGN_UP_SQL = """INSERT INTO public.customer(user_name, password, email, first_name, last_name, 
profile_picture_path) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');"""
ADMIN_USERNAME_SEARCH_SQL = """SELECT * FROM public.admin WHERE admin_user_name='{0}';"""
ADMIN_EMAIL_SEARCH_SQL = """SELECT * FROM public.admin WHERE email='{0}';"""
USER_USERNAME_SEARCH_SQL = """SELECT * FROM public.customer WHERE user_name='{0}';"""
USER_EMAIL_SEARCH_SQL = """SELECT * FROM public.customer WHERE email='{0}';"""
LOGS_SQL = """INSERT INTO public.logs(date, done_by, message, type) VALUES ('{0}', '{1}', '{2}', '{3}');"""
ADMINISTRATION_GET_USERS = """SELECT user_name, first_name, last_name, email FROM public.customer;"""
ADMINISTRATION_DELETE_USER = """DELETE FROM public.customer WHERE user_name='{0}';"""
