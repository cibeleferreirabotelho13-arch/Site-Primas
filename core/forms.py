from django import forms

from core.models import Mensagens


class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagens
        fields = (
            "nome",
            "data",
            "mensagem",
            "imagem",
        )

        labels = {  # noqa: RUF012
            "nome": "Nome do usuário",
            "data": "Data de publicação",
            "mensagem": "Mensagem",
            "imagem": "Imagem",
        }

        widgets = {  # noqa: RUF012
            "nome": forms.TextInput(
                attrs={
                    "required": True,
                }
            ),
            "data": forms.DateInput(
                attrs={
                    "required": True,
                    "type": "date",
                }
            ),
            "mensagem": forms.Textarea(
                attrs={
                    "required": True,
                    "rows": 6,
                }
            ),
            "imagem": forms.ClearableFileInput(),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get("nome")
        nome = nome.strip() if nome else ""

        if not nome:
            raise forms.ValidationError(
                "O nome é obrigatório."
            )

        return nome

    def clean_data(self):
        data = self.cleaned_data.get("data")
        data = data.strip() if data else ""

        if not data:
            raise forms.ValidationError(
                "A data é obrigatória."
            )

        return data

    def clean_mensagem(self):
        mensagem = self.cleaned_data.get("mensagem")
        mensagem = mensagem.strip() if mensagem else ""

        if not mensagem:
            raise forms.ValidationError(
                "A mensagem é obrigatória."
            )

       

        return mensagem