import django_tables2 as tables
from main.models.species import Species

def create_thumbnail_column(image_number):
    template = f'''
        {{% if record.image{image_number} %}}
            <img src="{{{{ record.image{image_number}.thumbnail }}}}"
                class="thumbnail"
                data-full="{{{{ record.image{image_number}.photo }}}}"
                data-title="<h2>{{% if record.specie__french_name %}}{{{{ record.specie__french_name }}}} - {{% endif %}}<i>{{{{ record.specie__latin_name }}}}</i></h2>"
                data-info="
                <p>Photo prise le {{{{ record.image{image_number}.date }}}}
                en {{{{ record.image{image_number}.country }}}}{{% if record.image{image_number}.region %}}({{{{ record.image{image_number}.region }}}}){{% endif %}}{{% if record.image{image_number}.details %}}. {{{{ record.image{image_number}.details }}}}{{% endif %}}
                </p>
                
                "
                alt="{{{{ record.specie__latin_name }}}}"
            >
        {{% endif %}}
    '''
    return tables.TemplateColumn(
        orderable=False,
        template_code=template,
        verbose_name=f"Photo {image_number}"
    )

italic = {"style": "font-style: italic;"}

class SpeciesTable(tables.Table):
    specie__latin_name = tables.Column(verbose_name="Nom latin", attrs={"td": italic})
    specie__french_name = tables.Column(verbose_name="Nom vernaculaire")
    specie__class_field = tables.Column(verbose_name="Classe", attrs={"td": italic})
    specie__order_field = tables.Column(verbose_name="Ordre", attrs={"td": italic})
    specie__family = tables.Column(verbose_name="Famille", attrs={"td": italic})
    min_year = tables.Column(verbose_name="Année")
    first_continent = tables.Column(visible=False)
    continent_list = tables.TemplateColumn(
        template_code="""
        {% for continent in record.continent_list %}
            {{ continent }}<br>
        {% endfor %}
        """,
        verbose_name="Continents",
        order_by="first_continent"
    )
    first_country = tables.Column(visible=False)
    country_list = tables.TemplateColumn(
        template_code="""
        {% for country in record.country_list %}
            {{ country }}<br>
        {% endfor %}
        """,
        verbose_name="Pays",
        order_by="first_country"
    )
    first_region = tables.Column(visible=False)
    region_list = tables.TemplateColumn(
        template_code="""
        {% for region in record.region_list %}
            {{ region }}<br>
        {% endfor %}
        """,
        verbose_name="Régions",
        order_by="first_region"
    )

    thumbnail1 = create_thumbnail_column(1)
    thumbnail2 = create_thumbnail_column(2)
    thumbnail3 = create_thumbnail_column(3)


    class Meta:
            model = Species
            template_name = "advanced_search_result/table.html"
            fields = ("specie__latin_name", "specie__french_name", "specie__class_field",
                      "specie__order_field", "specie__family", "min_year",
                      "continent_list", "country_list", "region_list",
                      "thumbnail1", "thumbnail2", "thumbnail3")
