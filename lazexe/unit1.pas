unit Unit1;

{$mode objfpc}{$H+}


interface

uses
  Classes, SysUtils, FileUtil, Forms, Controls, Graphics, Dialogs, Buttons,
  ExtCtrls;

type

  { TForm1 }

  TForm1 = class(TForm)
    fullButton: TSpeedButton;
    Timer3: TTimer;
    Timer4: TTimer;
    windButton: TSpeedButton;
    Timer1: TTimer;
    Timer2: TTimer;
    procedure FormCreate(Sender: TObject);
    procedure FormMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure FormMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
    procedure FormMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);

    procedure SpeedButton2Click(Sender: TObject);
    procedure fullButtonClick(Sender: TObject);

    procedure Timer3Timer(Sender: TObject);
    procedure Timer4Timer(Sender: TObject);
    procedure windButtonClick(Sender: TObject);
    procedure Timer2Timer(Sender: TObject);
    procedure SetShotInWindow;
  private

  FPressed : Boolean;
    FPosX, FPosY : Integer;
    FSizeCaption: Integer;
  public
    startDrag: boolean;
    X0, Y0: integer;
    os:string;
    x:string;
    path:string;

  end;

var
  Form1: TForm1;

implementation

{$R *.lfm}


{ TForm1 }
uses LCLType, LCLIntf    ;



procedure TForm1.SetShotInWindow;
var tmpBitmap:TBitmap;
    tmpHeight,tmpWidth:integer;
    ScreenDC: HDC;
      dirSeparator:char;
      namefile:string;
begin
  //ShowMessage(path);
  if Form1.x='win' then
     namefile:= Form1.path+'tmp.bmp'
  else
     namefile:= Form1.path+'tmp_f.bmp';

  ScreenDC := GetDC(0);
  tmpBitmap := TBitmap.Create;
  tmpBitmap.LoadFromDevice(ScreenDC);
  tmpBitmap.SaveToFile(nameFile);
  tmpBitmap.Free;
  Timer3.Enabled:=True;


end;

procedure TForm1.fullButtonClick(Sender: TObject);
begin
  Form1.WindowState:=wsMinimized;
  Timer3.Enabled:=False;
  Form1.x := 'full';

  Timer2.Enabled:=true;

end;



procedure TForm1.Timer3Timer(Sender: TObject);
var   file_name:string;
begin
  file_name := Form1.path+'flag.txt';
  if FileExists(file_name) then begin
     Form1.WindowState:=wsNormal;
  end
  else begin
     Form1.WindowState:=wsMinimized
  end;


end;

procedure TForm1.Timer4Timer(Sender: TObject);
var   file_name:string;
begin
    file_name := Form1.path+'is_work.txt';
  if not FileExists(file_name) then begin
     Application.Terminate;
  end;
end;

procedure TForm1.windButtonClick(Sender: TObject);
begin
  Form1.WindowState:=wsMinimized;
  Timer3.Enabled:=False;
  Form1.x := 'win';
  Timer2.Enabled:=true;

end;

procedure TForm1.Timer2Timer(Sender: TObject);
begin
    SetShotInWindow;
    Timer2.Enabled:=false;
end;

procedure TForm1.FormCreate(Sender: TObject);
begin
  os:='windows';
  {$IFDEF linux}
  os:='linux';
  {$ENDIF}

  Form1.path := ExtractFilePath(Application.ExeName);
  startDrag := False;
  form1.FormStyle:=fsSystemStayOnTop;
  width :=38;
  height := 120;
  form1.AlphaBlend:=true;
  form1.AlphaBlendValue:=127;{0-255}
  form1.Left := 30;
  form1.Top := 520;
  Timer3.Enabled:=True;
end;

procedure TForm1.FormMouseDown(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
 FPressed := True;
 FPosX := X;
 FPosY := Y;
end;

procedure TForm1.FormMouseMove(Sender: TObject; Shift: TShiftState; X,
  Y: Integer);
begin
   if FPressed then
  begin
    Left := Left - FPosX + X;
    Top := Top - FPosY + Y;
  end else begin
    if (abs(x-Width)<10) or (x<10) then  begin
       Cursor:=crSizeWE;
    end
    else begin
         Cursor:=crDefault;
    end;
  end;
end;

procedure TForm1.FormMouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
  FPressed := False;
end;



procedure TForm1.SpeedButton2Click(Sender: TObject);
begin
  Close;
end;



end.

