unit clipboard_unit1;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, FileUtil, Forms, Controls,
  Graphics, Dialogs, StdCtrls, Clipbrd, LCLIntf,
  LCLType, ExtCtrls;

type

  { TClipboard_Form1 }

  TClipboard_Form1 = class(TForm)
    Button1: TButton;
    Timer1: TTimer;

    procedure FormCreate(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
  private

  public

  end;

var
  Clipboard_Form1: TClipboard_Form1;

implementation

{$R *.lfm}

{ TClipboard_Form1 }






procedure TClipboard_Form1.Timer1Timer(Sender: TObject);
var clbBitmap:TBitmap;
  path,s,os,c:string;
  i,j: integer;
begin
     os:='windows';
  {$IFDEF linux}
  os:='linux';
  {$ENDIF}
  s:= ExtractFilePath(Application.ExeName);
  if os =  'windows' then c := '\' else c := '/';
  j := length(s);
  for i:=j-1 downto 1 do begin
      if s[i] = c then begin
         s := copy(s,1,i);
         break;
      end;
  end;


     clbBitmap:=TBitmap.Create;
     if Clipboard.HasFormat(CF_PICTURE) or Clipboard.HasFormat(CF_BITMAP)  then begin
          clbBitmap .Assign(Clipboard) ;
          clbBitmap.SaveToFile(s+'image.bmp');
          clbBitmap.Free;
     end;
     Application.Terminate;

end;

procedure TClipboard_Form1.FormCreate(Sender: TObject);
begin
  Clipboard_Form1.Visible:=False;
end;



end.

