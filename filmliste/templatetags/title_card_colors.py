from django import template
import json
register = template.Library()


@register.filter
def colorsJSON(value):
  """Returns a the colors of the list in a valid JSON format"""
  json_string = json.dumps(value.colors)
  return json_string
