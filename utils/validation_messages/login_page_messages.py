from utils.validation_messages.base_messages import BaseMessages


class LoginPageMessages(BaseMessages):
    """
    Validation messages for the login page
    """

    INVALID_EMAIL = "Le champ E-mail doit contenir une adresse e-mail valide."
    EMPTY_EMAIL = "Le champ E-mail est obligatoire."
    EMPTY_PASSWORD = "Le champ Mot de passe est obligatoire."
    WRONG_CREDENTIALS = "Votre compte n'a pas été trouvé. Veuillez réessayer svp"
    RESET_PASSWORD_SUCCESS = "Votre mot de passe a été modifié !"