from utils.validation_messages.base_messages import BaseMessages


class ResetPasswordPageMessages(BaseMessages):
    """
    validation messages for the reset password page
    """
    EMPTY_PASSWORD = "Le champ Mot de passe est obligatoire."
    EMPTY_PASSWORD_CONFIRMATION = "Le champ Confirmation du mot de passe est obligatoire."
    INVALID_PASSWORD = "Le mot de passe doit contenir au moins 8 caractères."
    INVALID_PASSWORD_CONFIRMATION = "Le champ Confirmation du mot de passe ne correspond pas."