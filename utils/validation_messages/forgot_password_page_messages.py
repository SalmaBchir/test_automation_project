from utils.validation_messages.base_messages import BaseMessages


class ForgotPasswordPageMessages(BaseMessages):
    """
       validation messages for the forgot password page
    """

    EMPTY_EMAIL = "Le champ E-mail est obligatoire."
    INVALID_EMAIL = "Le champ E-mail doit contenir une adresse e-mail valide."
    UNREGISTERED_EMAIL = "Le champ E-mail sélectionné est invalide."
    SUCCESS_MESSAGE = "Nous avons envoyé par e-mail le lien de réinitialisation de votre mot de passe!"

