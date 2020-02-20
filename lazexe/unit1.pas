unit Unit1;

{$mode objfpc}{$H+}


interface

uses
  Classes, SysUtils, FileUtil, Forms, Controls, Graphics, Dialogs, Buttons,
  ExtCtrls;

type

  { TForm1 }

  TForm1 = class(TForm)
    SpeedButton2: TSpeedButton;
    SpeedButton3: TSpeedButton;
    Timer1: TTimer;
    Timer2: TTimer;
    procedure FormCreate(Sender: TObject);
    procedure FormMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure FormMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
    procedure FormMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);

    procedure SpeedButton2Click(Sender: TObject);
    procedure SpeedButton3Click(Sender: TObject);
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
      namefile, path:string;
begin
  if os = 'linux' then
    dirSeparator := '/'
  else
    dirSeparator := '\';
  path := ExtractFilePath(Application.ExeName);

  //ShowMessage(path);
  namefile:= path+'tmp.bmp';
  ScreenDC := GetDC(0);
  tmpBitmap := TBitmap.Create;
  tmpBitmap.LoadFromDevice(ScreenDC);
  tmpBitmap.SaveToFile(nameFile);
  tmpBitmap.Free;
  Form1.Show;
end;

procedure TForm1.SpeedButton3Click(Sender: TObject);
begin
  Form1.Hide;
  SetShotInWindow;
  Timer2.Enabled:=true;
end;

procedure TForm1.Timer2Timer(Sender: TObject);
begin
      Form1.Show;
      Timer2.Enabled:=false;
end;

procedure TForm1.FormCreate(Sender: TObject);
begin
  os:='windows';
  {$IFDEF linux}
  os:='linux';
  {$ENDIF}
  startDrag := False;
  form1.FormStyle:=fsSystemStayOnTop;
  width :=38;
  height := 100;
  form1.AlphaBlend:=true;
  form1.AlphaBlendValue:=127;{0-255}
  form1.Left := 30;
  form1.Top := 590;
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

