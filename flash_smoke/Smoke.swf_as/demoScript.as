package 
{
	import flash.display.MovieClip;
	import fl.controls.Button;
	import fl.controls.Label;
	import fl.events.ComponentEvent;
	import flash.display.*;
	import flash.events.*;
	import flash.geom.*;
	import flash.text.*;
	import flash.events.MouseEvent;
	import fl.controls.Button;//MovieClip
	import flash.net.FileReference;
	import flash.net.FileReference.*;
	import flash.display.Bitmap;
	import flash.display.BitmapData;
	import flash.net.FileFilter;
	import flash.display.Loader;
	import flash.net.URLRequest;
	import flash.net.*;
	import 	fl.video.*;
	import flash.display.Sprite; 
	 import flash.text.TextField; 
	 import flash.text.TextFieldAutoSize; 
	 import flash.text.TextFormat; 
	public class demoScript extends flash.display.MovieClip
	{
		private var bt1:Button;
		private var file:FileReference=new FileReference();
		private var fileRef:FileReference= new FileReference();
		private var loader:Loader = new Loader();
		private var buttonShape:Shape = new Shape();
		//var loader.loader=new Loader();
		public function demoScript()
		{			
		   var textBox:TextField = new TextField(); 
			textBox.background=true;
		   textBox.text = "hello everd达式"; 
		   textBox.autoSize = TextFieldAutoSize.CENTER; 
		   textBox.embedFonts=true; 
		  // textBox.backgroundColor=0xff0000;
		   addChild(textBox); 
			
			var loc1:* = null;
			var loc2:* = null;
			var loc3:* = null;
			var loc4:* = null;
			//BGraund = new flash.display.Sprite();
			todSprite = new flash.display.Sprite();
			smoke = new smokeScript(350,-100,16711935,50,0.003);
			plz0 = new toddlerScript(80,30);
			plz1 = new toddlerScript(100,30);
			plz2 = new toddlerScript(255,50);//烟雾数值
			plz3 = new toddlerScript(255,50);
			plz4 = new toddlerScript(255,50);
			PachNFi = new flash.text.TextField();
			PachNFo = new flash.text.TextFormat();
			AlphaVFi = new flash.text.TextField();
			AlphaVFo = new flash.text.TextFormat();
			ColorPcRFi = new flash.text.TextField();
			ColorPcRFo = new flash.text.TextFormat();
			ColorPcGFi = new flash.text.TextField();
			ColorPcGFo = new flash.text.TextFormat();
			ColorPcBFi = new flash.text.TextField();
			ColorPcBFo = new flash.text.TextFormat();
			ColorPcFi = new flash.text.TextField();
			ColorPcFo = new flash.text.TextFormat();
			super();
			stage.frameRate = 40;
			//loc1 = new flash.geom.Matrix();
			//loc1.createGradientBox(590, 300, 0, 0, 0);
			//loc2 = [21504,602906];
			//loc3 = [1,1];
			//loc4 = [0,255];
			///BGraund.graphics.lineStyle(0.25, 0, 1);
			//BGraund.graphics.beginGradientFill(flash.display.GradientType.LINEAR, loc2, loc3, loc4, loc1);
			//BGraund.graphics.drawRect(0, 0, 590, 300);
			//BGraund.graphics.endFill();
			//addChild(BGraund);
			addChild(menu1);
			todSprite.addChild(plz0.toddlerShow(20, 235));
			PachNFo.bold = true;
			PachNFo.size = 16;
			PachNFo.color = 5592439;
			PachNFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(PachNFi);
			PachNFi.x = 20;
			PachNFi.y = 210;
			PachNFi.setTextFormat(PachNFo);
			todSprite.addChild(plz1.toddlerShow(20, 270));
			AlphaVFo.bold = true;
			AlphaVFo.size = 16;
			AlphaVFo.color = 5592439;
			AlphaVFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(AlphaVFi);
			AlphaVFi.x = 20;
			AlphaVFi.y = 245;
			AlphaVFi.setTextFormat(AlphaVFo);
			ColorPcFo.bold = true;
			ColorPcFo.size = 14;
			ColorPcFo.color = 5592439;
			ColorPcFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(ColorPcFi);
			ColorPcFi.x = 15;
			ColorPcFi.y = 60;
			ColorPcFi.setTextFormat(ColorPcFo);
			todSprite.addChild(plz2.toddlerShow(20, 100));
			ColorPcRFo.bold = true;
			ColorPcRFo.size = 14;
			ColorPcRFo.color = 5592439;
			ColorPcRFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(ColorPcRFi);
			ColorPcRFi.x = 20;
			ColorPcRFi.y = 80;
			ColorPcRFi.setTextFormat(ColorPcRFo);
			todSprite.addChild(plz3.toddlerShow(20, 140));
			ColorPcGFo.bold = true;
			ColorPcGFo.size = 14;
			ColorPcGFo.color = 5592439;
			ColorPcGFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(ColorPcGFi);
			ColorPcGFi.x = 20;
			ColorPcGFi.y = 120;
			ColorPcGFi.setTextFormat(ColorPcGFo);
			todSprite.addChild(plz4.toddlerShow(20, 180));
			ColorPcBFo.bold = true;
			ColorPcBFo.size = 14;
			ColorPcBFo.color = 5592439;
			ColorPcBFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(ColorPcBFi);
			ColorPcBFi.x = 20;
			ColorPcBFi.y = 160;
			ColorPcBFi.setTextFormat(ColorPcBFo);
			fon.graphics.lineStyle(1, 0, 1);
			fon.graphics.beginFill(3355443, 0);
			// fon.graphics.drawRect(0, 0, 800, 600);
			fon.graphics.endFill();
			addChild(fon);
			addChild(todSprite);
			addChild(smoke.FnSmoke());
			addEventListener(flash.events.Event.ENTER_FRAME, FnGoPl);
			//bt1.addEventListener(MouseEvent.CLICK, Kn);
			//addChild(bt1);
			Kn();
			//bt1.onButtonClick();
			return;
		}
			// buttonShapee = new Shape();


		//切换背景
		internal function Kn():void
		{
			// 开始您的自定义代码
			// 此示例代码在"输出"面板中显示"已单击鼠标"。
			//var file:FileReference=new FileReference();
			//设置文字
		   var textBox:TextField = new TextField(); 
			textBox.background=true;
		   textBox.text = "切换背景"; 
		   textBox.autoSize = TextFieldAutoSize.CENTER; 
		   textBox.embedFonts=true; 
		   //textBox.backgroundColor=0xff0000;
		   //addChild(textBox); 
		   var formatter:TextFormat = new TextFormat(); 
		      //formatter.font = "xjl"; 
			formatter.size = 30; 
		   
			 textBox.setTextFormat(formatter); 
		   
			buttonShape.graphics.beginFill(0x336699);
			//buttonShape.graphics.drawCircle(30, 25, 25);
			buttonShape.graphics.drawRect(20,10,120,25);
			
			var button = new SimpleButton(buttonShape,buttonShape,buttonShape,buttonShape);
			button.alpha = 0.5;
			addChild(button);
			button.addEventListener(MouseEvent.CLICK, onButtonClick);

			function onButtonClick(e:MouseEvent):void
			{
				fileRef.browse([new FileFilter("Images", "*.jpg;*.gif;*.png")]);
				fileRef.addEventListener(Event.SELECT, onFileSelected);
				

			}

			function onFileSelected(e:Event):void
			{
				//var loader:Loader = new Loader();
				// // loader.loadBytes(e.target.data);
									// // var bitmapData:BitmapData = _evt.target.content.bitmapData;
					
				
				
				//trace(loader.data);
				// var tempData:BitmapData=new BitmapData(loader.width,loader.height,
				                                                     // false,null);
				// tempData.draw(loader);
				// var bitmap:Bitmap = new Bitmap(tempData);
				
				// graphics.beginBitmapFill(Bitmap, new Matrix(), true, true);
					// graphics.drawRect(0, 0, stage.stageWidth, stage.stageHeight );

					// loader.contentLoaderInfo.removeEventListener(Event.COMPLETE , imageComplete);
					// loader = null;
				// addChild(bitmap);

				//
				fileRef.addEventListener(Event.COMPLETE, onFileLoaded);
				//fileRef.load();
				fileRef.load();
			}
			function test(e:Event):void
			{
				import flash.display.*;
				imgLoader("bg.jpg");
				var loader:Loader;
				function imgLoader(_path:String ):void
				{
					loader = new Loader  ;
					loader.contentLoaderInfo.addEventListener(Event.COMPLETE , imageComplete);
					loader.load(new URLRequest (_path));
					trace(loder);
				}
				function imageComplete(_evt:Event):void
				{
					var bitmapData:BitmapData = _evt.target.content.bitmapData;
					graphics.beginBitmapFill(bitmapData, new Matrix(), true, true);
					graphics.drawRect(0, 0, stage.stageWidth, stage.stageHeight );

					loader.contentLoaderInfo.removeEventListener(Event.COMPLETE , imageComplete);
					loader = null;
				}
			}

			function onFileLoaded(e:Event):void
			{
					
				//
				fileRef.removeEventListener(Event.COMPLETE,onFileLoaded);
				loader.contentLoaderInfo.addEventListener(Event.COMPLETE,onLoadComplete);
				loader.loadBytes(fileRef.data);
				//trace(loader.data);
				// var tempData:BitmapData=new BitmapData(loader.width,loader.height,
				                                                     // false,null);
				// tempData.draw(loader);
				// var bitmap:Bitmap = new Bitmap(tempData);
				// addChild(bitmap);

				//addChild(loader);
			}
		function onLoadComplete(e:Event):void
		{
			trace(stage.width,stage.height,loader.width,loader.height);
			var tempData:BitmapData=new BitmapData(570,300,  //loder.
										false,null);
			//loader.scaleMode=StageScaEXACT_FIT;
			loader.content.width=400	;
			loader.content.height=300;
			tempData.draw(loader); //绘画
			//var bitmap:Bitmap = new Bitmap(tempData); //转换类型
			// addChild(bitmap);
			// loader.contentLoaderInfo.removeEventListener(Event.COMPLETE,
			                                                     // onLoadComplete);
																 
				// var bitmapData:BitmapData = _evt.target.content.bitmapData;
				mtr = new Matrix();
				mtr.tx=170;
				//mtr.a = stage.width/loader.width;
				//mtr.d = stage.height/loader.height;
					 graphics.beginBitmapFill(tempData, mtr, true, true);
					 graphics.drawRect(170, 0, 400, 300 );//stageHeight 舞台大小变化小 两height变化大
					 loader.contentLoaderInfo.removeEventListener(Event.COMPLETE , onLoadComplete);
					 // loader = null;
		}
			//*/
			//trace("已单击鼠标");
			//trace(fileRef);
			//var directory:File = new File ; 
			// 结束您的自定义代码
		}


		internal function FnGoPl(arg1:flash.events.Event):void
		{
			var loc1:* = undefined;
			var loc2:* = undefined;
			var loc3:* = undefined;
			var loc4:* = undefined;
			var loc5:* = undefined;
			var loc6:* = undefined;
			smoke.PachN = plz0.nmb + 20;
			PachNFi.text = "PachN" + ":  " + smoke.PachN;
			PachNFi.setTextFormat(PachNFo);
			smoke.AlphaV = plz1.nmb / 10000;
			AlphaVFi.text = "AlphaV" + ":  " + plz1.nmb / 10000;
			AlphaVFi.setTextFormat(AlphaVFo);
			smoke.ColorR = plz2.nmb;
			smoke.ColorG = plz3.nmb;
			smoke.ColorB = plz4.nmb;
			ColorPcRFi.text = "redOffset" + ":  " + plz2.nmb;
			ColorPcRFi.setTextFormat(ColorPcRFo);
			ColorPcGFi.text = "greenOffset" + ":  " + plz3.nmb;
			ColorPcGFi.setTextFormat(ColorPcGFo);
			ColorPcBFi.text = "blueOffset" + ":  " + plz4.nmb;
			ColorPcBFi.setTextFormat(ColorPcBFo);
			loc1 = Math.floor(plz2.nmb / 16);
			loc2 = plz2.nmb % 16;
			loc3 = Math.floor(plz3.nmb / 16);
			loc4 = plz3.nmb % 16;
			loc5 = Math.floor(plz4.nmb / 16);
			loc6 = plz4.nmb % 16;
			ColorPcFi.text = "ColorPc" + ":  " + "0x" + loc1.toString(16) + loc2.toString(16) + loc3.toString(16) + loc4.toString(16) + loc5.toString(16) + loc6.toString(16);
			ColorPcFi.setTextFormat(ColorPcFo);
			return;
		}


		{
			fon = new flash.display.Sprite();
		};

		internal var ColorPcFi:flash.text.TextField;

		internal var plz3:toddlerScript;

		internal var ColorPcGFo:flash.text.TextFormat;

		internal var ColorPcGFi:flash.text.TextField;

		internal var plz2:toddlerScript;

		internal var BGraund:flash.display.Sprite;

		internal var ColorPcRFi:flash.text.TextField;

		internal var ColorPcBFi:flash.text.TextField;

		internal var smoke:smokeScript;

		internal var ColorPcRFo:flash.text.TextFormat;

		internal var todSprite:flash.display.Sprite;

		internal var ColorPcBFo:flash.text.TextFormat;

		public var menu1:flash.display.MovieClip;

		internal var PachNFi:flash.text.TextField;

		internal var PachNFo:flash.text.TextFormat;

		internal var AlphaVFi:flash.text.TextField;

		internal var AlphaVFo:flash.text.TextFormat;

		//internal var bt1:Button;

		internal var plz0:toddlerScript;

		internal var plz1:toddlerScript;

		internal var plz4:toddlerScript;

		internal var ColorPcFo:flash.text.TextFormat;

		public static var fon:flash.display.Sprite;
	}
}