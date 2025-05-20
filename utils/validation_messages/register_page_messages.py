from utils.validation_messages.base_messages import BaseMessages


class RegisterPageMessages(BaseMessages):
    """
    Validation messages for the register page
    """

    INVALID_EMAIL = "Le champ E-mail doit contenir une adresse e-mail valide."
    INVALID_PASSWORD = "Le mot de passe doit contenir au moins 8 caractères."
    INVALID_PASSWORD_CONFIRMATION = "Le champ Confirmation du mot de passe ne correspond pas."
    EMPTY_LASTNAME = "Le champ Nom est obligatoire."
    EMPTY_FIRSTNAME = "Le champ Prénom est obligatoire."
    EMPTY_EMAIL = "Le champ E-mail est obligatoire."
    EMPTY_PASSWORD = "Le champ Mot de passe est obligatoire."
    ALREADY_REGISTERED = "L'adresse e-mail est déjà utilisée."