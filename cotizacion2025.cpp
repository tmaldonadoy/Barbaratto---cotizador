#include <iostream>
using namespace std;

void doceC();
void DiecisieteC();
void veinteC();
void cinta();
void film();
void ccorr();

int main()
{
string a;
cout<<"Que desea cotizar? (cajas/cinta/film/ccorr)"<<endl;
cin>>a;
if (a=="cajas")
{
    string b,d;
    bool c;
    c=true;
    while(c)
	{
    cout<<"Que tipo de caja desea cotizar? (12c/17c/20c)"<<endl;
    cin>>b;
    if (b=="12c")
    {
        doceC();
        cout<<"Quiere serguir cotizando? (si/no)"<<endl;
        cin>>d;
        if(d=="si")
		{
			c=true;
		}
		else if(d=="no")
		{
			c=false;
		}
    }
    else if (b=="20c")
    {
        veinteC();
        cout<<"Quiere serguir cotizando? (si/no)"<<endl;
        cin>>d;
        if(d=="si")
		{
			c=true;
		}
		else if(d=="no")
		{
			c=false;
		}
    }
    else if (b=="17c")
    {
        DiecisieteC();
        cout<<"Quiere serguir cotizando? (si/no)"<<endl;
        cin>>d;
        if(d=="si")
		{
			c=true;
		}
		else if(d=="no")
		{
			c=false;
		}
    }
   }
}
else if (a=="cinta")
{
    cinta();
}
else if (a=="film")
{
    film();
}
else if (a=="ccorr")
{
    ccorr();
}
system("PAUSE");
return 0;
}
void doceC()
{
 double precio,costo;
 int largo, ancho, alto,m1,m11;
 float m2;
 cout<<"Introduzca medidas en milimetros Largo/ancho/alto"<<endl;
 cin>>largo;
 cin>>ancho;
 cin>>alto;
 m1=ancho+alto+50;
  if(m1<300)
  {
      m1=300;
  }
 m11=((largo+ancho)*2+80);
 if(m11>1710 and m11<1899)
 {
     m11=1900;
 }
 m2=m11*m1;
 m2=m2/1000000;
 costo=m2*440;
 if(largo==300 and ancho==200 and alto==120 )
  {
     precio=320;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
  }
 else if(largo==180 and ancho==80 and alto==180 )
  {
     precio=212;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
  }
 else if(largo==600 and ancho==400 and alto==400 )
  {
     precio=1054;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
  }
 else if (largo==500 and ancho==400 and alto==300)
 {
     precio=1080;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
 }
  else if (largo==420 and ancho==420 and alto==350)
 {
     precio=970;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
 }
  else if (largo==400 and ancho==300 and alto==300)
 {
     precio=704;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
 }
 else if (largo==300 and ancho==230 and alto==300)
 {
     precio=465;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
 }
  else if (largo==300 and ancho==200 and alto==250)
 {
     precio=423;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
 }
  else if (largo==300 and ancho==200 and alto==200)
 {
     precio=362;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
 }
  else if (largo==260 and ancho==180 and alto==250)
 {
     precio=369;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
 }
  else if (largo==200 and ancho==150 and alto==200)
 {
     precio=247;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
 }
  else if (largo==100 and ancho==100 and alto==150)
 {
     precio=115;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
 }
  else if (largo==100 and ancho==100 and alto==110)
 {
     precio=120;
     cout<<"El precio es: $"<< precio<<" +iva (caja STOCK)"<<endl;
 }
  else if (largo==140 and ancho==100 and alto==150)
 {
     precio=322;
     cout<<"El precio de la/las caja/s autoarmable/s es: "<< precio<<" +iva (caja STOCK)"<<endl;
 }
 else
 {
     string b;
     cout<<"Es con impresion? (si/no)"<<endl;
     cin>>b;
     if(b=="si")
     {
         int c;
         cout<<"La impresion a un color es de 2 o 4 caras? (2/4)"<<endl;
         cin>>c;
         if(c==2)
         {
             costo=costo+26.7;
         }
         else if (c==4)
         {
             costo=costo+39.3;
         }
     }
  if(costo>0 and costo<70)
  {
     precio=costo+70;
      cout<<"El precio es: $"<< precio<<" +iva"<<endl;
      cout<<"La cantidad de cajas tiene que ser mayor a 1000"<<endl;

  }
  if(costo>=70 and costo<100)
  {
     precio=costo+100;
        cout<<"El precio es: $"<< precio<<" +iva"<<endl;
        cout<<"La cantidad de cajas tiene que ser mayor a 500"<<endl;

  }
  if(costo>=100 and costo<150)
  {
     precio=costo+115;
        cout<<"El precio es: $"<< precio<<" +iva"<<endl;
        cout<<"La cantidad de cajas tiene que ser mayor a 400"<<endl;
  }
  if(costo>=150 and costo<653)
  {
     precio=costo*1.84;
        cout<<"El precio es: $"<< precio<<" +iva"<<endl;
        cout<<"La cantidad de cajas tiene que ser mayor a 300"<<endl;

  }
  if(costo>=653 and costo<900)
  {
     precio=costo*1.7;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
  }
  else if(costo>=900 and costo<1000)
  {
     precio=costo*1.69;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
     cout<<"R2"<<endl;

  }
 }
}
void veinteC()
{

 double precio,costo;
 int largo, ancho, alto,m1,m11;
 float m2;
 cout<<"Introduzca medidas en milimetros Largo/ancho/alto"<<endl;
 cin>>largo;
 cin>>ancho;
 cin>>alto;
 m1=ancho+alto+50;
  if(m1<300)
  {
      m1=300;
  }
 m11=((largo+ancho)*2+80);
 if(m11>1690 and m11<1890)
 {
     m11=1900;
 }
 m2=m11*m1;
 m2=m2/1000000;
 costo=m2*650;
 string b;
 cout<<"Es con impresion? (si/no)"<<endl;
 cin>>b;
    if(b=="si")
     {
         int c;
         cout<<"La impresión a un color es de 2 o 4 caras? (2/4)"<<endl;
         cin>>c;
         if(c==2)
         {
             costo=costo+26.7;
         }
         else if (c==4)
         {
             costo=costo+39.3;
         }
     }
  if(costo>0 and costo<70)
  {
     precio=costo+70;
        cout<<"El precio es: $"<< precio<<" +iva"<<endl;
        cout<<"La cantidad de cajas tiene que ser mayor a 1000"<<endl;

  }
  if(costo>=70 and costo<100)
  {
     precio=costo+100;
        cout<<"El precio es: $"<< precio<<" +iva"<<endl;
        cout<<"La cantidad de cajas tiene que ser mayor a 500"<<endl;
  }
  if(costo>=100 and costo<150)
  {
     precio=costo+115;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
     cout<<"La cantidad de cajas tiene que ser mayor a 400"<<endl;
  }
  if(costo>=150 and costo<700)
  {
     precio=costo*1.84;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
     cout<<"La cantidad de cajas tiene que ser mayor a 300"<<endl;
  }
  if(costo>=700 and costo<900)
  {
     precio=costo*1.7;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
  }
  else if(costo>=900 and costo<1000)
  {
     precio=costo*1.69;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
     cout<<"La cantidad de cajas tiene que ser mayor a 500"<<endl;
  }
    else if(costo>=1000 and costo<1500)
  {
     precio=costo*1.5;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
     cout<<"La cantidad de cajas tiene que ser mayor a 500"<<endl;
  }
 }
 void DiecisieteC()
{

 double precio,costo;
 int largo, ancho, alto,m1,m11;
 float m2;
 cout<<"Introduzca medidas en milimetros Largo/ancho/alto"<<endl;
 cin>>largo;
 cin>>ancho;
 cin>>alto;
 m1=ancho+alto+50;
  if(m1<300)
  {
      m1=300;
  }
 m11=((largo+ancho)*2+80);
 if(m11>1690 and m11<1890)
 {
     m11=1900;
 }
 m2=m11*m1;
 m2=m2/1000000;
 costo=m2*540;
 string b;
 cout<<"Es con impresion? (si/no)"<<endl;
 cin>>b;
    if(b=="si")
     {
         int c;
         cout<<"La impresión a un color es de 2 o 4 caras? (2/4)"<<endl;
         cin>>c;
         if(c==2)
         {
             costo=costo+26.7;
         }
         else if (c==4)
         {
             costo=costo+39.3;
         }
     }
  if(costo>0 and costo<70)
  {
     precio=costo+70;
        cout<<"El precio es: $"<< precio<<" +iva"<<endl;
        cout<<"La cantidad de cajas tiene que ser mayor a 1000"<<endl;

  }
  if(costo>=70 and costo<100)
  {
     precio=costo+100;
        cout<<"El precio es: $"<< precio<<" +iva"<<endl;
        cout<<"La cantidad de cajas tiene que ser mayor a 500"<<endl;
  }
  if(costo>=100 and costo<150)
  {
     precio=costo+115;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
     cout<<"La cantidad de cajas tiene que ser mayor a 400"<<endl;
  }
  if(costo>=150 and costo<700)
  {
     precio=costo*1.84;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
     cout<<"La cantidad de cajas tiene que ser mayor a 300"<<endl;
  }
  if(costo>=700 and costo<900)
  {
     precio=costo*1.71;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
  }
  else if(costo>=900 and costo<1500)
  {
     precio=costo*1.65;
     cout<<"El precio es: $"<< precio<<" +iva"<<endl;
     cout<<"La cantidad de cajas tiene que ser mayor a 500"<<endl;
  }
 }
void cinta()
{
    int precio;
    precio=570;
    cout<<"El precio es de : $"<<precio<<" +iva"<<endl;
}
void film()
{
    string a;
    cout<<"Film transparente o negro (t/n)"<<endl;
    cin>>a;
    int precio;
    if(a=="t")
    {
       precio=3450;
       cout<<"El precio es de : $"<<precio<<" +iva"<<endl;
    }
    else if(a=="n")
    {
        precio=4050;
        cout<<"El precio es de : $"<<precio<<" +iva"<<endl;
    }
}
void ccorr()
{
    int cantidad, precio;
    cout<<"Ingrese la cantidad de rollos de 120 de 40kg"<<endl;
    cin>>cantidad;
    precio=890*40;
    cout<<"El precio de : $"<<cantidad*precio<<" +iva"<<endl;
}
