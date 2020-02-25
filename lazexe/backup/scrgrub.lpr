program scrgrub;

{$mode objfpc}{$H+}

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads,
  {$ENDIF}{$ENDIF}
  Interfaces, // this includes the LCL widgetset
  Forms,  Unit1    , Windows  {Закоментувати для Linux}
  { you can add units after this };


{$R *.res}
Var
 MemHnd : HWND;

begin
  {Закоментувати для Linux}
  MemHnd := CreateFileMapping(HWND($FFFFFFFF),
                              nil,
                              PAGE_READWRITE,
                              0,
                              10,
                              'temp');
  if GetLastError=ERROR_ALREADY_EXISTS then Exit;
  {-----------------------------}


  Application.Initialize;
  Application.CreateForm(TForm1, Form1);


  Application.Run;
end.

