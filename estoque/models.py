from django.db import models

# Create your models here.
from django.db import models

class Ingrediente(models.Model):
    nome = models.CharField(max_length=100)
    unidade = models.CharField(max_length=20) # Ex: Kg, Litro, unidade
    meta = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_atual = models.DecimalField(max_digits=10, decimal_places=2)
    consumo_real = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Preencher caso o ingrediente tenha faltado")
    
    # Flags para as regras de negócio
    vencido = models.BooleanField(default=False, help_text="O ingrediente estragou/venceu?")
    faltou_antes_do_fim = models.BooleanField(default=False, help_text="Acabou antes do mês terminar?")

    def __str__(self):
        return self.nome