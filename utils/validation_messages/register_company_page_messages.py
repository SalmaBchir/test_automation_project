from utils.validation_messages.base_messages import BaseMessages


class RegisterCompanyPageMessages(BaseMessages):
    """
    Validation messages for the register company page
    """

    INVALID_EMAIL = "Le champ E-mail doit être une adresse email valide."
    EMPTY_NAME = "Le champ nom est obligatoire."
    EMPTY_SIRET = "Le champ siret est obligatoire."
    EMPTY_EMAIL = "Le champ E-mail est obligatoire."
    ALREADY_REGISTERED = "La valeur du champ E-mail est déjà utilisée."

