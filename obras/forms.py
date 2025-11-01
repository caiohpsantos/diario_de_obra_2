import json
from django import forms
from django.contrib.gis.geos import GEOSGeometry
from .models import Obras
from contratos.models import Contratos


# no topo do arquivo
import json
from django.contrib.gis.geos import GEOSGeometry, Polygon
from django import forms

class formCadastraObra(forms.ModelForm):
    """
    Classe responsável pela criação do formulário de cadastro de novas obras.
    Campos: situacao, contrato, nome, local, inicio, termino, empresa_responsavel e area
    """
    # declara explicitamente o campo oculto que receberá WKT/GeoJSON/JSON-array
    area = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Obras
        fields = ['situacao', "contrato", "nome", "local", "inicio", "termino", "empresa_responsavel","area"]
        widgets = {
            "inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "termino": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "empresa_responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "situacao": forms.Select(attrs={"class": "form-select"}),
            "contrato": forms.Select(attrs={"class": "form-select"}),
        }
        input_formats = {
            "inicio": ["%Y-%m-%d"],
            "termino": ["%Y-%m-%d"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contrato'].queryset = Contratos.objects.filter(ativo=True)

    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        if Obras.objects.filter(nome=nome).exists():
            raise forms.ValidationError("Este nome de obra já está em uso.")
        return nome

    def _coords_list_from_possible_array(self, parsed):
        """
        Recebe um parsed Python object (lista de listas, possivelmente lat-lng ou lng-lat)
        Retorna lista de pares [lng, lat] (pronta para montar WKT).
        """
        # esperamos parsed = [ [a,b], [a,b], ... ] ou [[[a,b],...] (caso envolto)
        # normalize:
        arr = parsed
        # se for [[[...]]] tirar um nível
        if isinstance(arr, list) and len(arr) and isinstance(arr[0][0], list):
            arr = arr[0]

        pairs = []
        for item in arr:
            if not (isinstance(item, (list, tuple)) and len(item) >= 2):
                continue
            a = float(item[0])
            b = float(item[1])
            pairs.append([a, b])

        if not pairs:
            return None

        # Heurística: Geo coordinate ranges: lat in [-90,90], lon in [-180,180].
        # If first value of pairs looks like lat (abs>90) and second abs<=90, swap.
        # More robust: check majority of values
        count_lat_like = sum(1 for x, y in pairs if abs(x) <= 90 and abs(y) > 90)
        count_lon_like = sum(1 for x, y in pairs if abs(x) > 90 and abs(y) <= 90)

        # If appears to be [lat,lon], convert to [lon,lat]
        if count_lat_like > count_lon_like:
            pairs = [[lng, lat] for lat, lng in pairs]

        # Now ensure pairs are [lon, lat]
        return pairs

    def clean_area(self):
        """
        Aceita:
         - WKT string: 'POLYGON ((lng lat, ...))'
         - GeoJSON geometry string ({"type":"Polygon","coordinates":[...]})
         - JSON array string: [[lat,lng],...] ou [[lng,lat],...]
        Retorna: GEOSGeometry polygon com srid=4326 ou None.
        """
        data = self.cleaned_data.get("area")
        if not data:
            return None

        # Strip whitespace
        s = data.strip()

        # 1) Se aparenta ser WKT (começa por POLYGON ou MULTIPOLYGON etc.)
        if s.upper().startswith("POLYGON") or s.upper().startswith("MULTIPOLYGON"):
            try:
                geom = GEOSGeometry(s)
                # garantir SRID
                if getattr(geom, "srid", None) is None:
                    geom.srid = 4326
                elif geom.srid != 4326:
                    geom.transform(4326)
                return geom
            except Exception as e:
                raise forms.ValidationError(f"WKT inválido: {e}")

        # 2) Se parece ser GeoJSON (objeto)
        if s.startswith("{") or s.startswith('['):
            # tenta decodificar JSON
            try:
                parsed = json.loads(s)
            except Exception as e:
                raise forms.ValidationError(f"GeoJSON/JSON inválido: {e}")

            # se for GeoJSON geometry/dict contendo 'type' e 'coordinates'
            if isinstance(parsed, dict) and parsed.get("type") and parsed.get("coordinates") is not None:
                try:
                    # GEOS aceita GeoJSON string diretamente
                    geom = GEOSGeometry(json.dumps(parsed))
                    if getattr(geom, "srid", None) is None:
                        geom.srid = 4326
                    elif geom.srid != 4326:
                        geom.transform(4326)
                    return geom
                except Exception as e:
                    raise forms.ValidationError(f"GeoJSON inválido: {e}")

            # se for array de coordenadas
            coords_pairs = self._coords_list_from_possible_array(parsed)
            if not coords_pairs:
                raise forms.ValidationError("Array de coordenadas inválido para 'area'.")

            # Gera WKT a partir das coordenadas (assegura fechamento do anel)
            # coords_pairs currently are [lon, lat] pairs
            if coords_pairs[0] != coords_pairs[-1]:
                coords_pairs.append(coords_pairs[0])
            wkt_coords = ", ".join(f"{lng} {lat}" for lng, lat in coords_pairs)
            wkt = f"POLYGON(({wkt_coords}))"
            try:
                geom = GEOSGeometry(wkt)
                geom.srid = 4326
                return geom
            except Exception as e:
                raise forms.ValidationError(f"Não foi possível criar geometria a partir das coordenadas: {e}")

        raise forms.ValidationError("Formato de área desconhecido. Envie WKT, GeoJSON ou array JSON de coordenadas.")


class formEditaObra(forms.ModelForm):
    """
    Classe responsável pela criação do formulário de edição de obras.
    Campos: situacao, contrato, nome, local, inicio, termino, empresa_responsavel, area
    """

    # Campo oculto para armazenar o WKT da geometria
    area = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Obras
        fields = [
            "situacao",
            "contrato",
            "nome",
            "local",
            "inicio",
            "termino",
            "empresa_responsavel",
            "area",
        ]
        widgets = {
            "inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "termino": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "empresa_responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "situacao": forms.Select(attrs={"class": "form-select"}),
            "contrato": forms.Select(attrs={"class": "form-select"}),
        }

        input_formats = {
            "inicio": ["%Y-%m-%d"],
            "termino": ["%Y-%m-%d"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtra contratos ativos
        contratos_qs = Contratos.objects.filter(ativo=True)

        # Se estiver editando uma obra existente, inclui o contrato atual mesmo se estiver inativo
        if self.instance and getattr(self.instance, "pk", None) and getattr(self.instance, "contrato", None):
            contrato_atual = self.instance.contrato
            if contrato_atual and not contrato_atual.ativo:
                contratos_qs = Contratos.objects.filter(pk=contrato_atual.pk) | contratos_qs

        self.fields["contrato"].queryset = contratos_qs

        # Se a obra já possui área, preenche o hidden com o WKT
        if self.instance and getattr(self.instance, "area", None):
            try:
                self.fields["area"].initial = self.instance.area.wkt
            except Exception:
                self.fields["area"].initial = ""

    def clean_nome(self):
        nome = self.cleaned_data.get("nome")
        instance = getattr(self, "instance", None)

        # Se for um novo registro (sem instance.id)
        if not instance or not instance.pk:
            if Obras.objects.filter(nome=nome).exists():
                raise forms.ValidationError("Este nome de obra já está em uso.")
        else:
            # Se for edição, só valida se o nome mudou
            if nome != instance.nome:
                if Obras.objects.filter(nome=nome).exists():
                    raise forms.ValidationError("Este nome de obra já está em uso.")

        return nome

    def clean_area(self):
        """
        Aceita:
         - WKT string: 'POLYGON ((lng lat, ...))'
         - GeoJSON geometry string ({"type":"Polygon","coordinates":[...]})
         - JSON array string: [[lat,lng],...] ou [[lng,lat],...]
        Retorna: GEOSGeometry polygon com srid=4326 ou None.
        """
        data = self.cleaned_data.get("area")
        if not data:
            return None

        # Strip whitespace
        s = data.strip()

        # 1) Se aparenta ser WKT (começa por POLYGON ou MULTIPOLYGON etc.)
        if s.upper().startswith("POLYGON") or s.upper().startswith("MULTIPOLYGON"):
            try:
                geom = GEOSGeometry(s)
                # garantir SRID
                if getattr(geom, "srid", None) is None:
                    geom.srid = 4326
                elif geom.srid != 4326:
                    geom.transform(4326)
                return geom
            except Exception as e:
                raise forms.ValidationError(f"WKT inválido: {e}")

        # 2) Se parece ser GeoJSON (objeto)
        if s.startswith("{") or s.startswith('['):
            # tenta decodificar JSON
            try:
                parsed = json.loads(s)
            except Exception as e:
                raise forms.ValidationError(f"GeoJSON/JSON inválido: {e}")

            # se for GeoJSON geometry/dict contendo 'type' e 'coordinates'
            if isinstance(parsed, dict) and parsed.get("type") and parsed.get("coordinates") is not None:
                try:
                    # GEOS aceita GeoJSON string diretamente
                    geom = GEOSGeometry(json.dumps(parsed))
                    if getattr(geom, "srid", None) is None:
                        geom.srid = 4326
                    elif geom.srid != 4326:
                        geom.transform(4326)
                    return geom
                except Exception as e:
                    raise forms.ValidationError(f"GeoJSON inválido: {e}")

            # se for array de coordenadas
            coords_pairs = self._coords_list_from_possible_array(parsed)
            if not coords_pairs:
                raise forms.ValidationError("Array de coordenadas inválido para 'area'.")

            # Gera WKT a partir das coordenadas (assegura fechamento do anel)
            # coords_pairs currently are [lon, lat] pairs
            if coords_pairs[0] != coords_pairs[-1]:
                coords_pairs.append(coords_pairs[0])
            wkt_coords = ", ".join(f"{lng} {lat}" for lng, lat in coords_pairs)
            wkt = f"POLYGON(({wkt_coords}))"
            try:
                geom = GEOSGeometry(wkt)
                geom.srid = 4326
                return geom
            except Exception as e:
                raise forms.ValidationError(f"Não foi possível criar geometria a partir das coordenadas: {e}")

