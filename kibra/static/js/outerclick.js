//http://cpojer.net/blog/Custom_outerClick_event
Element.Events.outerClick = {
	
	base : 'click',
	
	condition : function(event){
		event.stopPropagation();
		return false;
	},
	
	onAdd : function(fn){
		this.getDocument().addEvent('click', fn);
	},
	
	onRemove : function(fn){
		this.getDocument().removeEvent('click', fn);
	}
	
};