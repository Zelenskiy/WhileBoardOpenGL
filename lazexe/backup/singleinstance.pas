unit SingleInstance;
{$mode objfpc}{$H+}

//  en: The only program instance using named global MUTEX
//  ru: Единственный экземпляр программы используя именованный глобальный объект MUTEX


//  en: InstanceActivate - Register program instance or activate previous instance and stop program execution
//  ru: InstanceActivate - Зарегистрировать экземпляр программы или активировать предыдущий экземпляр и остановить выполнение программы
procedure   InstanceActivate (AppIdName:string);


//  en: InstanceClose - Unregister program instance
//  ru: InstanceClose - Дерегистрация экземпляра программы
procedure   InstanceClose;


implementation


procedure   InstanceActivate (ApplicationID:string);
var
    Window:THandle;
begin
    Mutex:=CreateMutex(nil,true,PChar('Global\'+ApplicationID));
    if GetLastError = ERROR_ALREADY_EXISTS then
    begin
        Window:=FindWindow('TForm1', 'Form1');
        ShowWindow(Window,SW_RESTORE);
        SetForegroundWindow(Window);
        Halt;
    end;
end;


procedure   InstanceClose;
begin
    CloseHandle(Mutex);
end;


end.

