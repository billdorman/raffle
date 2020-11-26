(function($) {
	var pluginName='raffleDrumAnimation',
		init_arr=[],
		defaults={
			itemImage:[],
			loop:false,
			spinning:false,
			drumSpeed:0,
			drumSpeedIncrease:.001,
			drumSpeedMax:.1,
			drumGap:0,
			drumY:50,
			drumRadiusX:0,
			drumRadiusY:50,
			itemRow:7,
			itemColumn:5,
			itemColumnStartX:5,
			itemWidth:15,
			itemGap:0,
			itemY:40,
			itemRadiusX:2,
			itemRadiusY:33,
			displayNumber:false,
			displayNumberExclude:[],
			result:false,
			callback:''
        };
	
	/*!
	 * 
	 * INIT - This is the function that runs to init
	 * 
	 */
	$.fn[pluginName]=function(options,value) {
		if(typeof options=='string'){
			var $this=$(this);
			var _opts=$this.data('plugin_'+pluginName);
			if(_opts!=undefined)
				$.fn[pluginName].commandRaffleAnimation(this,options,value)
		}else{
			return this.each(function () {
				var $this=$(this);
				var _opts=$this.data('plugin_'+pluginName);
				$.fn[pluginName].destroy($this);
				
				var _opts=$.extend({},defaults,options);
				$this.data('plugin_' + pluginName, _opts);
				
				init_arr.push($this.attr('id'));
				$.fn[pluginName].initAniamtion($this);
			});
		}
	}
	
	/*!
	 * 
	 * START BUILD CANVAS - This is the function that runs to build canvas
	 * 
	 */
	$.fn[pluginName].initAniamtion=function(obj) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data('plugin_'+pluginName);
			
			var sideLength = _self.find('.drumSideHolder .side').length;
			_opts.drumGap = 100 / sideLength;
	
			_self.find('.drumSideHolder .side').each(function(index, element) {
				$(element).attr('data-angle', index * ((Math.PI * 2) / sideLength));
			});
			
			_self.find('.itemsWrapper').empty();
			$.fn[pluginName].generateItems(_self);
			$.fn[pluginName].updateOffset(_self);
			
			$.fn[pluginName].updateSpinData(_self);
			//$.fn[pluginName].animateItemsFall(_self, false, false);
		});
    }
	
	/*!
	 * 
	 * FISHES - This is the function that runs to create fishes
	 * 
	 */
	 $.fn[pluginName].generateItems=function(obj) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data( 'plugin_' + pluginName);
			
			var itemSpace = (100 - (_opts.itemColumnStartX*2)) / _opts.itemColumn;
			_opts.itemGap = 100 / _opts.itemRow;
			var startX = 0;
			
			for(var n=0; n<_opts.itemRow; n++){
				_self.find('.itemsWrapper').append('<div class="items"></div>');
				
				startX = _opts.itemColumnStartX;
			
				for(var t=0; t<_opts.itemColumn; t++){
					var randomX = randomIntFromInterval(-5,5);
					var randomY = randomIntFromInterval(-5,5);
					
					var itemNum = Math.round(Math.random()*(_opts.itemImage.length-1));
					var itemDegree = Math.round(Math.random()*360);
					
					var itemHTML = $('<div class="item" style="width:'+_opts.itemWidth+'%; left:'+((startX)+randomX)+'%; top:'+randomY+'%; transform: rotate('+itemDegree+'deg);"><img src="'+_opts.itemImage[itemNum]+'" /></div>');
					itemHTML.attr('data-top', randomY);
					itemHTML.attr('data-left', (startX)+randomX);
					
					startX += itemSpace;
					_self.find('.itemsWrapper .items').eq(n).append(itemHTML);
				}
				
				_self.find('.itemsWrapper .items').eq(n).attr('data-reset', 'true');
				_self.find('.itemsWrapper .items').eq(n).attr('data-angle', n * ((Math.PI * 2) / _opts.itemRow));
				_self.find('.itemsWrapper .items').eq(n).attr('data-offset', randomIntFromInterval(0,40));
			}
			
			if(_opts.displayNumber){
				_self.find('.itemsWrapper .item').each(function(index, element) {
					var numberHTML = '<div class="displayNumber">'+index+'</div>'
					$(this).append(numberHTML);
				});
			}
		});
    }
	
	$.fn[pluginName].updateOffset=function(obj) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data( 'plugin_' + pluginName);
			
			_self.find('.items').each(function(index, element) {
				var currentAngle = Number($(element).attr('data-angle'));
				var currentTop = (Math.sin(currentAngle) * _opts.itemRadiusY);
				var offset = (_opts.itemRadiusY - currentTop);
				
				var randomNum = randomIntFromInterval(0,offset/1.5);
				$(element).attr('data-offset', randomNum);
			});
		});
    }
	
	/*!
	 * 
	 * UPDATE FISHES - This is the function that runs to updated fishes
	 * 
	 */
	$.fn[pluginName].updateSpinData=function(obj) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data( 'plugin_' + pluginName);
			
			var offsetRange = 100;
			if(_opts.spinning){
				_opts.drumSpeed += _opts.drumSpeedIncrease;
				_opts.drumSpeed = _opts.drumSpeed > _opts.drumSpeedMax ? _opts.drumSpeedMax : _opts.drumSpeed;
				//$.fn[pluginName].animateItemsFall(_self, true, true);
			}else{
				_opts.drumSpeed -= _opts.drumSpeedIncrease;
				_opts.drumSpeed = _opts.drumSpeed < 0 ? 0 : _opts.drumSpeed;
				offsetRange = 50;
				//$.fn[pluginName].animateItemsFall(_self, true, false);
			}
			
			var currentProgress = 0;
			_self.find('.drumSideHolder .side').each(function(index, element) {
				var currentAngle = Number($(element).attr('data-angle'));
				var currentTop = Math.sin(currentAngle) * _opts.drumRadiusY;
				var currentLeft = Math.cos(currentAngle) * _opts.drumRadiusX;
				var currentScaleLeft = Math.cos(currentAngle) * 2;
				var scale = (currentScaleLeft / _opts.drumRadiusY)+1;
				
				$(element).css('left', (currentLeft)+'%');
				$(element).css('top', currentTop+_opts.drumY+'%');
				
				if(scale >= 1){
					$(element).show();
				}else{
					$(element).hide();	
				}
				
				$(element).attr('data-angle', currentAngle += _opts.drumSpeed);
			});
			
			var currentProgress = 0;
			var sortArray = [];
			_self.find('.itemsWrapper .items').each(function(index, element) {
				var currentOffset = Number($(element).attr('data-offset'));
				var currentAngle = Number($(element).attr('data-angle'));
				var currentLeft = (Math.cos(currentAngle) * _opts.itemRadiusX);
				var currentTop = (Math.sin(currentAngle) * _opts.itemRadiusY);
				
				var percent = offsetRange - (Math.round(_opts.drumSpeed * (offsetRange * 10)));
				var offset = (_opts.itemRadiusY - (currentTop+currentOffset))/offsetRange * percent;
				
				$(element).css('left', (currentLeft)+'%');
				$(element).css('top', (currentTop + offset)+_opts.itemY+'%');
				
				$(element).attr('data-angle', currentAngle += _opts.drumSpeed);
				
				var scale = (currentLeft / _opts.itemRadiusY)+1;
				sortArray.push({index:index, scale:scale});
				
				$(element).css('transform', 'scale(' + scale + ')');
				
				if(currentTop < 0){
					$(element).attr('data-reset', 'false');
				}else if(currentTop >= (_opts.itemRadiusY-10) && $(element).attr('data-reset') == 'false'){
					$(element).attr('data-reset', 'true');
					$.fn[pluginName].rotateItems(_self, index);	
				}
			});
			
			sortOnObject(sortArray, 'scale', false);
			for(var n=0; n<sortArray.length; n++){
				var thisIndex = sortArray[n].index;
				_self.find('.itemsWrapper .items').eq(thisIndex).css('z-index', n);	
			}
			
			if(!_opts.spinning && _opts.drumSpeed <= 0 && _opts.result){
				$.fn[pluginName].animateResult(_self);
			}
			
			if(_opts.loop)
				$.fn[pluginName].loopSpin(_self);
			
		});
    }
	
	$.fn[pluginName].toggleSpin=function(obj, con) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data( 'plugin_' + pluginName);
			
			_self.find('.ticketResult').hide();
			if(con != undefined){
				if(_opts.spinning){
					_self.find('.item').each(function(index, element) {
						$(element).stop( true, true );
					});
				}
				
				if(!con){
					$.fn[pluginName].updateOffset(_self);	
				}
				_opts.spinning = con;
			}else{
				if(_opts.spinning){
					$.fn[pluginName].updateOffset(_self);
					_self.find('.item').each(function(index, element) {
						$(element).stop( true, true );
					});
					_opts.spinning = false;
				}else{
					_opts.spinning = true;
				}
			}
			
			if(!_opts.loop){
				_opts.loop = true;
				$.fn[pluginName].loopSpin(_self);
			}
			
		});
    }
	
	$.fn[pluginName].loopSpin=function(obj) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data( 'plugin_' + pluginName);
			
			_self.find('.raffleHolder').animate({
				opacity: 1
			}, 10, function() {
				$.fn[pluginName].updateSpinData(_self);
			});
		});
    }
	
	$.fn[pluginName].rotateItems=function(obj, target) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data( 'plugin_' + pluginName);
			
			if(!_opts.spinning){
				return;	
			}
			
			_self.find('.items').eq(target).attr('data-offset', randomIntFromInterval(0,40));
				
			_self.find('.items').eq(target).find('.item').each(function(index, element) {
				var randomSpeed = (Math.random()*2) + 1;
				
				$(element).animate(
					{ deg: Math.round(Math.random()*360) },
					{
					  duration: randomSpeed * 1000,
					  step: function(now) {
						$(this).css({ transform: 'rotate(' + now + 'deg)' });
					  }
					}
				  );
			});
		});
    }
	
	$.fn[pluginName].animateItemsFall=function(obj, animate, con) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data( 'plugin_' + pluginName);
			
			_self.find('.items').each(function(index, element) {
				var currentAngle = Number($(element).attr('data-angle'));
				var currentTop = (Math.sin(currentAngle) * _opts.itemRadiusY);
				var offset = _opts.itemRadiusY - currentTop;
				
				$(element).find('.item').each(function(index2, element2) {
					if(!con){
						if(animate){	
							$(element2).css('top', offset);
						}else{
							$(element2).css('top', offset);	
						}
					}else{
						$(element2).css('top', Number($(element2).attr('data-top'))+'%');
					}
				});
			});
		});
    }
	
	$.fn[pluginName].animateResult=function(obj) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data( 'plugin_' + pluginName);
			
			_self.find('.ticketResult').show();
			_opts.result = false;
			var itemNum = Math.round(Math.random()*(_opts.itemImage.length-1));
			var itemDegree = Math.round(Math.random()*360);
			
			var randomX = randomIntFromInterval(30,50);
			var itemHTML = $('<div class="item" style="width:'+_opts.itemWidth+'%; left:'+randomX+'%; top:'+50+'%; transform: rotate('+itemDegree+'deg);"><img src="'+_opts.itemImage[itemNum]+'" /></div>');
			
			_self.find('.ticketResult').css('z-index','auto');
			_self.find('.ticketResult').empty();
			_self.find('.ticketResult').append(itemHTML);
			
			if(_opts.displayNumber){
				var randomNumber = Math.round(Math.random()*(_opts.itemRow * _opts.itemColumn));
				var numberHTML = '<div class="displayNumber">'+randomNumber+'</div>';
				_self.find('.ticketResult .item').append(numberHTML);
			}
			
			$.fn[pluginName].callbackRaffle(_self,'result');
			_self.find('.ticketResult .item').animate({top:'-50%'}, {
				duration: 1000,
				complete: function () {
					_self.find('.ticketResult').css('z-index',1000);
					_self.find('.ticketResult .item').css('transform', 'scale(' + 1.5 + ')');
				
				  _self.find('.ticketResult .item').animate({top:'35%'}, {
					duration: 1000,
					complete: function () {
					  $.fn[pluginName].callbackRaffle(_self,'resultcomplete');
					}
				  });
				}
			  });
		});
    }
	
	$.fn[pluginName].callbackRaffle=function(obj,command,con) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data( 'plugin_' + pluginName);
			con=con==undefined?true:con
			if($.isFunction(_opts.callback)&&con){
				var returnData=_opts
				returnData.status=command
				returnData.id=_self.attr('id');
				_opts.callback(returnData);
			}
		});
    }

	/*!
	 * 
	 * UPDATE FISH ANIMATION SETTINGS - This is the function that runs to update fish animation settings
	 * 
	 */
	$.fn[pluginName].commandRaffleAnimation=function(obj,command,value){
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data('plugin_'+pluginName);
			
			if(init_arr.indexOf(_self.attr('id')) != -1){
				_opts.result = false;
				
				switch(command) {
					case 'destroy':
							$.fn[pluginName].destroy(_self);
						break;
					case 'toggleSpin':
							$.fn[pluginName].toggleSpin(_self);
						break;
					case 'spin':
							$.fn[pluginName].toggleSpin(_self, true);
						break;
					case 'stop':
							$.fn[pluginName].toggleSpin(_self, false);
						break;
					case 'result':
							_opts.result = true;
							if(_opts.spinning){
								$.fn[pluginName].toggleSpin(_self, false);
							}else{
								$.fn[pluginName].animateResult(_self);
							}
						break;
					default:
						if(_opts[value]!=undefined){
							//_opts[value]=value2;
							
							if(value == 'spin'){
								//alert('spin')
								//$.fn[pluginName].updateFishes(_self, 'number');
							}
						}
				}
			}
		});
	}
	
	/*!
	 * 
	 * DESTROY FISH ANIMATION - This is the function that runs to destroy fish animation
	 * 
	 */
	$.fn[pluginName].destroy=function(obj) {
		return obj.each(function(){
			var _self=$(this);
			var _opts=_self.data('plugin_'+pluginName);
			
			if(_opts != undefined){
				_opts.result = false;
				_opts.spinning = false;
				_opts.loop = false;
				_opts.drumSpeed = 0;
				_opts.displayNumberExclude = [];
				
				_self.find('.item').each(function(index, element) {
					$(element).stop( true, true );
				});
				
				_self.find('.raffleHolder').stop( true, true );
				
				_self.find('.itemsWrapper').empty();
				_self.find('.ticketResult').empty();
				
				var indexNum = init_arr.indexOf(_self.attr('id'));
				init_arr.splice(indexNum, 1);
			}
		});
    }
	
	function randomIntFromInterval(min,max){
		return Math.floor(Math.random()*(max-min+1)+min);
	}
	
	function sortOnObject(array, object, rev) {
		if(rev){
			array.sort(function(a, b){
				var a1= a[object], b1= b[object];
				if(a1== b1) return 0;
				return a1< b1? 1: -1;
			});
		}else{
			array.sort(function(a, b){
				var a1= a[object], b1= b[object];
				if(a1== b1) return 0;
				return a1> b1? 1: -1;
			});
		}
		return array;
	}

})(jQuery);