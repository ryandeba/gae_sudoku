$(function(){

	var Cell = Backbone.Model.extend({
		defaults: {
			value: "",
			isSelected: false
		},

		initialize: function(){
			var self = this;
			self.listenTo(self, "set:value", self.validateValue);
		},

		validateValue: function(){
			var self = this;
			if (self.get("value") == "" || "123456789".indexOf(self.get("value")) == -1){
				self.set("value", "")
			}
		}
	});

	var CellView = Backbone.View.extend({
		tagName: "div",

		template:  _.template($("#cellTemplate").html()),

		attributes: {
			"class" : "sudoku-cell"
		},

		events: {
			"click": "clickListener"
		},

		initialize: function(){
			this.listenTo(this.model, "change", this.render);
			this.listenTo(this.model, "change:value", this.valueChanged);
		},

		clickListener: function(){
			this.model.trigger("selectCell", this.model);
		},

		valueChanged: function(){
			var self = this;
			setTimeout(function(){
				self.flippyFlippy();
			}, 1);
		},

		render: function(){
			this.$el.html(this.template(this.model.toJSON()));

			if (this.model.collection.length == 81
				&& [3,4,5,12,13,14,21,22,23,27,28,29,33,34,35,36,37,38,42,43,44,45,46,47,51,52,53,57,58,59,66,67,68,75,76,77]
					.indexOf(this.model.collection.indexOf(this.model)) > -1){
				this.$el.addClass('sudoku-group-cell-2');
			}

			if (this.model.get("isSelected")){
				this.$el.addClass("is-selected");
			} else {
				this.$el.removeClass("is-selected");
			}

			return this;
		},

		//TODO: also did this drunk
		flippyFlippy: function(){
			var self = this;
			self.$el.addClass("animated flipInY");
			setTimeout(function(){
				self.$el.removeClass("animated flipInY");
			}, 1000);
		}
	});

	var Cells = Backbone.Collection.extend({
		model: Cell,

		initialize: function(){
			var self = this;
			for (var i = 0; i < 81; i++){
				self.add({});
			}

			self.listenTo(self, "change:isSelected", self.changeIsSelectedListener);
		},

		changeIsSelectedListener: function(changedCell){
			var self = this;
			if (changedCell.get("isSelected")){
				self.each(function(cell){
					if (cell != changedCell){
						cell.set("isSelected", false);
					}
				});
			}
		}
	});

	var App = Backbone.View.extend({

		events: {
			"keypress": "keypressListener",
			"click .js-solve-button": "solveBoard",
			"click .js-clear-button": "clearBoard",
			"click .js-new-button": "newPuzzle",
			"click .js-gamemode-play-button": "clickGameModePlayButton",
			"click .js-gamemode-solve-button": "clickGameModeSolveButton",
			"click .js-close-options-button": "closeOptions"
		},

		initialize: function(){
			var self = this;

			self.cells = new Cells();
			self.cells.at(0).set("isSelected", true);
			self.listenTo(self.cells, "selectCell", self.selectCell);
			
			var controlsJSON = [];
			for (var i = 1; i < 10; i++){
				controlsJSON.push({'value': i.toString()});
				if (i == 9) {
					controlsJSON.push({"value": "C"});
				}
			}
			self.controls = new Cells(controlsJSON);
			self.listenTo(self.controls, "selectCell", self.controlClicked);

			self.setGameMode("play");
		},

		setGameMode: function(mode){
			var self = this;
			if (self.gameMode == "play" && mode == "solve"){
			}
			else if (self.gameMode == "solve" && mode == "play"){
			}
			self.gameMode = mode;
		},

		clickGameModePlayButton: function(){
			this.setGameMode("play");
		},

		clickGameModeSolveButton: function(){
			this.setGameMode("solve");
		},

		closeOptions: function(){
			this.$el.find("#optionsPanel").panel("close");
		},

		clearBoard: function(){
			var self = this;
			self.cells.each(function(cell){
				cell.set("value", "");
			});
			self.cells.at(0).set("isSelected", true);
		},

		keypressListener: function(eventData){
			var self = this;
			self.setSelectedCellToValue(self.convertKeyCodeToSudokuValue(eventData.keyCode));
		},

		convertKeyCodeToSudokuValue: function(keyCode){
			switch (keyCode){
				case 49:
					return "1";
				case 50:
					return "2";
				case 51:
					return "3";
				case 52:
					return "4";
				case 53:
					return "5";
				case 54:
					return "6";
				case 55:
					return "7";
				case 56:
					return "8";
				case 57:
					return "9";
				default:
					return "";
			}
		},

		controlClicked: function(control){
			var self = this;
			if ("123456789C".indexOf(control.get("value")) > -1){
				self.setSelectedCellToValue(control.get("value"));
			}
		},

		setSelectedCellToValue: function(value){
			var self = this;
			value = "123456789".indexOf(value) > -1 ? value : "";
			self.cells.findWhere({"isSelected" : true}).set("value", value);
			self.selectNextCell();
		},

		selectNextCell: function(){
			var self = this;
			var indexOfCurrentSelectedCell = self.cells.indexOf(self.cells.findWhere({"isSelected" : true}));
			var nextCell = indexOfCurrentSelectedCell < 80 ? indexOfCurrentSelectedCell + 1 : 0;
			self.cells.at(nextCell).set("isSelected", true);
		},

		selectCell: function(cell){
			cell.set("isSelected", true);
		},

		newPuzzle: function(){
			var self = this;
			$.ajax({
				url: "/newPuzzle",
				success: function(data){ self.receiveNewPuzzle(data); }
			});
		},

		receiveNewPuzzle: function(data){
			var self = this;
			data = data[0].split("");
			self.cells.each(function(cell, iterator){
				cell.set("value", data[iterator]);
			});
		},

		solveBoard: function(){
			var self = this;

			var board = "";

			self.cells.each(function(cell){
				board += cell.get("value").length == 1 ? cell.get("value") : "0";
			});

			self.$el.find("#message").html("Solving...");

			$.ajax({
				url: "/solveBoard?board=" + board,
				success: function(data){ self.receiveSolutions(data); }
			});
		},

		receiveSolutions: function(data){
			var self = this;
			self.$el.find("#message").html("");
			if (data[0].length == 0){
				self.$el.find("#message").html("No possible solution");
			}
			for (var i = 0; i < data[0].length; i++){
				(function(x){
					setTimeout(function(){
						self.cells.at(x).set("value", data[0].charAt(x));
					}, x * 30);
				}(i));
			}
		},

		render: function(){
			this.renderBoard();
			this.renderControls();
			return this;
		},

		renderBoard: function(){
			var self = this;
			var $board = self.$el.find("#board");
			$board.html("");
			self.cells.each(function(cell, iterator){
				if (iterator % 9 == 0) {
					$board.append("<div class='sudoku-row'></div>");
				}
				var cellView = new CellView({model: cell});
				$board.find(".sudoku-row").last().append(cellView.render().$el);
			});
		},

		renderControls: function(){
			var self = this;
			var $controls = self.$el.find("#controls");
			$controls.html("");
			self.controls.each(function(cell, iterator){
				if (iterator % 9 == 0){
					$controls.append("<div class='sudoku-row'></div>");
				}
				var cellView = new CellView({model: cell});
				$controls.find(".sudoku-row").last().append(cellView.render().$el);
			});
		}
	});

	new App({
		el: "body"
	}).render();

	var resizeElements = function(){
		var sudokuCellSize = ($(window).width() - 30 - (5 * 8)) / 9;
		if ($(window).height() < $(window).width() * 1.25) {
			sudokuCellSize = ($(window).height() - 10) / 12.5;
		}
		less.modifyVars({
			'@sudoku-cell-size' : sudokuCellSize + 'px'
		});
	};
	resizeElements();
	$(window).on("resize", function(){
		resizeElements();
	});
});
