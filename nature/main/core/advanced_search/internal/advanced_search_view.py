from main.core.advanced_search.internal.forms import SpeciesSearchForm


def advanced_search(request):
        form = SpeciesSearchForm(request.GET or None)
        return form