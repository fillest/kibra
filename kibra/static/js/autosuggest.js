
var App = window.App || {};

//var l = l || console.log;  //TODO dont do that, always check if console present

App.Autosuggest = new Class({
	Implements: [Options, Log, Class.Occlude/*, Events*/],

	Binds: ["select", "choose", "on_key_down", "on_key_up"],

	options: {
		debug: false,
		max_matches: 16
	},

	initialize: function (element, options) {
		if (this.occlude("widget", element)) return this.occluded;

		this.setOptions(options);
		this.options.debug && this.enableLog();

		this.element = $(element); //TODO rename to input_element
		this.value_old = this.element.get("value");
		this.dropdown_element = Elements.from(
			'<div class="autosuggest-dropdown">' +
				'<ul></ul>' +
			'</div>'
		)[0].inject(document.body);
		this.is_shown = false;

		this.setup();
	},
	
	setup: function () {
		this.element.addEvents({
			keydown: this.on_key_down,
			keyup: this.on_key_up,
			outerClick: function (_e) {this.hide();}.bind(this)
		});
	},

	hide: function () {
		if (this.is_shown) {
			this.dropdown_element.hide();
			this.is_shown = false;
		}
	},

	parse_tag_at_caret: function (input) {
		var matches = this.parse_input(input);
		var cpos = this.element.getCaretPosition();
		var cur = null;
		matches.each(function (item) {
			if ((cpos >= item.start) && (cpos <= item.end)) cur = item;
		});
		return cur;
	},

	choose: function () {
		//TODO del duplicates tags
		//-- cut out them and all non-tag (and non-filter?) text + repose caret
		var val = this.element.get("value");
		var cur = this.parse_tag_at_caret(val);
		cur && this.element.selectRange(cur.start, cur.end);
		this.element.insertAtCursor(this.matches[this.cur_i].name + " ", false)
		this.hide();
	},

	on_key_down: function (e) {
		switch (e.key) {
			case "enter":
			case "tab":
				if (this.is_shown) {
					this.choose();
					return false; //*no effect in opera
				}
				break;
			case "up":
				this.is_shown && this.select_prev();
				break;
			case "down":
				if (this.is_shown) {
					this.select_next();
				} else {
					var cur = this.parse_tag_at_caret(this.element.get("value"));
					cur && this.show(cur.tag);
				}
				break;
			case "esc":
				this.hide();
				break;
			default:
				break;
		}
	},

	on_key_up: function (e) {
		var val = this.element.get("value");
		var cur = this.parse_tag_at_caret(val);

		if (this.value_old != val) {
			this.value_old = val;
			if (cur) {
				this.show(cur.tag);
			} else {
				this.hide();
			}
		} else {
			//TODO track caret  <-- what?
		}
	},

	match: function (input) {
        var norm_input = input.toLowerCase();
        
		var matches = App.all_tags.map(function (tag_name) {
			var rank = levenshtein(tag_name, norm_input);

			if (tag_name.test('^' + norm_input.escapeRegExp())) rank -= 3;

			norm_input.split('').unique().each(function (letter) {
				var re = new RegExp(letter.escapeRegExp(), 'g');
				var c1 = $pick(tag_name.match(re), []).length,
					c2 = $pick(norm_input.match(re), []).length;
				rank += c1 ? -1 : 1;
				if (c1 && c2 && (c1 == c2)) rank -= 1;
			});

			return {weight: rank, name: tag_name};
		});

		matches.sort(function (tag1, tag2) {return tag1.weight - tag2.weight;});
		return matches.slice(0, this.options.max_matches);
	}.protect(),

	parse_input: function (input) {
		var match,
            tag_regexp = /[^\s,\.\-]+/g,
            matches = [];
		while ((match = tag_regexp.exec(input)) != null) {
			matches.push({
				tag: match[0],
				start: match.index,
				end: match.index + match[0].length
			});
		}
		return matches;
	}/*.protect()*/,

	select: function (i) {
//		console.log(this.caller._origin);

		if ($defined(this.cur_i)) {
			this.matches_ui[this.cur_i].removeClass("hover");
		}

		this.cur_i = i;

		this.matches_ui[i].addClass("hover");
	},

	select_prev: function () {
//		console.log('select_prev()');
		if (this.cur_i) this.select(this.cur_i - 1);
	},

	select_next: function () {
//		console.log('select_next()');
		if (this.cur_i != (this.matches_ui.length - 1)) this.select(this.cur_i + 1);
	},

	show: function (input) {
//		console.log('show()');
		this.matches = this.match(input);
		this.matches_ui = [];

		if (this.matches.length) {
			this.matches.each(function (match, i) {
				this.matches_ui.push(new Element("li").adopt(
					Element("span", {
						html: (match.name)
//						html: (match.weight + " " + match.name)
						      .replace(input, "<strong>" + input + "</strong>"),
						events: {
//							mouseover: this.select.pass(i),
							click: function () {
								this.select(i);
								this.choose();
							}.bind(this)
						}
					})
				));
			}.bind(this));

			this.dropdown_element.getElement('ul').empty().adopt(this.matches_ui);

			this.select(0);

			var c = this.element.getCoordinates();
			this.dropdown_element.setStyles({
				top: c.top + c.height + "px",
				left: c.left + 5 + "px"
			}).show();
			this.is_shown = true;
		}
	}
});