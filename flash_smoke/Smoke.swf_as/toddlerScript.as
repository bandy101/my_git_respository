package 
{
    import flash.display.*;
    import flash.events.*;
    
    public class toddlerScript extends flash.display.Sprite
    {
        public function toddlerScript(arg1:*, arg2:*)
        {
            toddlerSprite = new flash.display.Sprite();
            bzpl = new flash.display.Sprite();
            plz = new flash.display.Sprite();
            pl = new PZl();
            pl1 = new PZl1();
            bz = new BZl();
            bz1 = new BZl1();
            flagPlz = 0;
            range = 100;
            super();
            bzpl.addChild(bz);
            bzpl.addChild(bz1);
            bz1.visible = false;
            plz.addChild(pl1);
            plz.addChild(pl);
            pl.visible = false;
            plz.addEventListener(flash.events.MouseEvent.MOUSE_DOWN, FnPlzGo);
            demoScript.fon.addEventListener(flash.events.MouseEvent.MOUSE_UP, FnPlzStop);
            plz.addEventListener(flash.events.MouseEvent.MOUSE_UP, FnPlzStop1);
            plz.addEventListener(flash.events.MouseEvent.MOUSE_OVER, FnPlagPlzOn);
            plz.addEventListener(flash.events.MouseEvent.MOUSE_OUT, FnPlagPlzOff);
            nmb = arg2;
            nmp = arg2;
            range = arg1;
            return;
        }

        internal function FnPlzStop1(arg1:flash.events.MouseEvent):void
        {
            removeEventListener(flash.events.Event.ENTER_FRAME, FnFnPlzGoG);
            pl.visible = false;
            bz1.visible = false;
            return;
        }

        public function toddlerShow(arg1:*, arg2:*):flash.display.Sprite
        {
            bzpl.x = arg1;
            bzpl.y = arg2;
            plz.x = arg1 + 100 * nmp / range;
            plz.y = arg2;
            pozPlzS = arg1;
            pozPlzF = arg1 + 100;
            toddlerSprite.addChild(bzpl);
            toddlerSprite.addChild(plz);
            return toddlerSprite;
        }

        internal function FnPlzStop(arg1:flash.events.MouseEvent):void
        {
            removeEventListener(flash.events.Event.ENTER_FRAME, FnFnPlzGoG);
            pl.visible = false;
            bz1.visible = false;
            return;
        }

        internal function FnPlagPlzOff(arg1:flash.events.MouseEvent):void
        {
            flagPlz = 0;
            return;
        }

        internal function FnFnPlzGoG(arg1:flash.events.Event):void
        {
            plz.x = mouseX;
            if (mouseX <= pozPlzS) 
            {
                plz.x = pozPlzS;
            }
            if (mouseX >= pozPlzF) 
            {
                plz.x = pozPlzF;
            }
            nmb = range * (plz.x - pozPlzS) / 100;
            return;
        }

        internal function FnPlagPlzOn(arg1:flash.events.MouseEvent):void
        {
            flagPlz = 1;
            return;
        }

        internal function FnPlzGo(arg1:flash.events.MouseEvent):void
        {
            if (flagPlz == 1) 
            {
                addEventListener(flash.events.Event.ENTER_FRAME, FnFnPlzGoG);
                pl.visible = true;
                bz1.visible = true;
            }
            return;
        }

        public function toddlerNum():int
        {
            return nmb;
        }

        public var plz:flash.display.Sprite;

        internal var pozPlzS:int;

        internal var pozPlzF:int;

        internal var pl:PZl;

        internal var range:int=100;

        internal var bzpl:flash.display.Sprite;

        internal var bz:BZl;

        internal var toddlerSprite:flash.display.Sprite;

        public var nmb:int;

        public var nmp:int;

        internal var pl1:PZl1;

        internal var bz1:BZl1;

        internal var flagPlz:int=0;
    }
}
