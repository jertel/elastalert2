"""Enhancement to reformat `top_events_X`

from match in order to reformat and put it
back to be able to use in alert message.
New format:

top_events_keys_XXX -- contains array of corresponding key values defined in `top_count_keys`,
  where `XXX` key from `top_count_keys` array.
top_events_values_XXX -- contains array of corresponding counts.

Example:
  Original:
    {"top_events_KEY.NAME":{"key_value1": 10, "key_value2": 20}}

  Reformatted:
    {
      "top_events_keys_KEY.NAME":["key_value1", "key_value2"]
      "top_events_values_KEY.NAME":[10, 20]
    }

Can be used in the rule like:
top_count_keys:
  - 'KEY.NAME'
match_enhancements:
  - 'elastalert_modules.top_count_keys_enhancement.Enhancement'
alert_text_args:
  - top_events_keys_KEY.NAME[0]
"""
from elastalert.enhancements import BaseEnhancement


class Enhancement(BaseEnhancement):
    def process(self, match):
        top_count_keys = self.rule['top_count_keys']
        if top_count_keys:
            for k in top_count_keys:
                key = "top_events_%s" % k
                if match[key]:
                    filtered = {key: value for (key, value) in match[key].items() if key}
                    match["top_events_keys_%s" % k] = list(filtered.keys())
                    match["top_events_values_%s" % k] = list(filtered.values())
