program clpbrd;
uses
  Classes, SysUtils,  Forms, Controls, Graphics, Dialogs, StdCtrls, Clipbrd, LCLIntf,
  LCLType, ExtCtrls;

var clbBitmap:TBitmap;

begin
     clbBitmap:=TBitmap.Create;
     if Clipboard.HasFormat(CF_PICTURE) then begin
          clbBitmap .Assign(Clipboard) ;
          clbBitmap.SaveToFile('image.bmp');
          clbBitmap.Free;
     end;
end.

