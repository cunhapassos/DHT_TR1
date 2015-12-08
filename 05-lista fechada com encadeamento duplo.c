// lista fechada com encadeamento duplo
#include <stdio.h>
#include <stdlib.h>

typedef struct elemento {
  char dado;
  struct elemento *prox, *ant;
} listaD;

/*------ procedimentos deste conjunto--

void ConstroiListaFD1(listaD **epinicio)
void ConstroiListaFD(listaD **epinicio)
void PercorreListaFD(listaD *pinicio) 
void *ProcuraListaFD(listaD *pinicio, char chave)
void InsereListaFD(listaD **epinicio, char dadonovo)
void RemoveListaFD(listaD **epinicio, char chave)
void DestroiListaFD(listaD **epinicio)
--------------------------------------*/

//--------------------------------------------
void ConstroiListaFD1(listaD **epinicio) {
  FILE *arq;
  listaD *p1;
  char c;

  arq = fopen ("t5.txt", "r");
  *epinicio = NULL;
  while (((c = getc (arq)) != EOF) && (c != '\n')) {
    p1 = malloc (sizeof (listaD));
    p1->dado = c;
    if (*epinicio == NULL) {
      p1->prox = p1;
      p1->ant = p1;
      *epinicio = p1;
    }
    else {
      p1->prox = *epinicio;
      p1->ant = (*epinicio)->ant;
      (*epinicio)->ant->prox = p1;
      (*epinicio)->ant = p1;
      *epinicio = p1;
    }  
  }
  fclose (arq);
}

//--------------------------------------------
void ConstroiListaFD(listaD **epinicio) {
  FILE *arq;
  listaD *p1, *p2;
  char c;
  
  arq = fopen ("t5.txt", "r");
  *epinicio = NULL;
  while (((c = getc (arq)) != EOF) && (c != '\n')) {
    p1 = malloc (sizeof (listaD));
    p1->dado = c;
    if (*epinicio == NULL) { 
      p1->prox = p1;
      p1->ant = p1;
      *epinicio = p1;
    }  
    else {
      p1->prox = *epinicio;
      p1->ant = p2;
      p2->prox = p1;
      (*epinicio)->ant = p1;
    }  
    p2 = p1;
  }
  fclose (arq);
}

//--------------------------------------------
void PercorreListaFD(listaD *pinicio) {
  listaD *p1;

  if (pinicio == NULL)
    printf ("lista vazia \n");
  else {          
    p1 = pinicio;     
    do {
      printf("elemento:  %c \n", p1->dado);
      p1 = p1->prox;   
    }
    while (p1 != pinicio);
    do {
      p1 = p1->ant; 
      printf("elemento (para tras):  %c \n", p1->dado);
    }
    while (p1 != pinicio);
  }     
}
    
//--------------------------------------------
void *ProcuraListaFD(listaD *pinicio, char chave) {
  listaD *p1;
   
  if (pinicio == NULL)
    p1 = NULL;
  else {
    p1 = pinicio;     
    do
      p1 = p1->prox;     
    while ((p1 != pinicio) && (p1->dado != chave));
    if ((p1 == pinicio) && (p1->dado != chave))
      p1 = NULL;
  }
  return p1;
}

//--------------------------------------------
void InsereListaFD(listaD **epinicio, char dadonovo){
  listaD *p1, *p2;
       
  p1 = malloc (sizeof (listaD));
  p1->dado = dadonovo;
  if (*epinicio == NULL) {
    p1->prox = p1;
    p1->ant = p1;
    *epinicio = p1;
  }
  else
    if ((*epinicio)->dado > dadonovo) {
      p1->prox = *epinicio;
      p1->ant = (*epinicio)->ant;
      (*epinicio)->ant->prox = p1;
      (*epinicio)->ant = p1;
      *epinicio = p1;
    }
    else {
      p2 = *epinicio;     
      while ((p2->prox != *epinicio) && (p2->prox->dado < dadonovo))
        p2 = p2->prox; 
      p1->prox = p2->prox;
      p1->ant = p2;
      p2->prox->ant = p1;      
      p2->prox = p1;   
    }       
}

//--------------------------------------------
void RemoveListaFD(listaD **epinicio, char chave){
  listaD *p1, *p2;
         
  if (*epinicio == NULL)
    printf("lista vazia \n");
  else {
    while ((*epinicio != NULL) && ((*epinicio)->dado == chave)) {
      if ((*epinicio)->prox == *epinicio) {
        free (*epinicio);
        *epinicio = NULL;
      }
      else {
        p1 = *epinicio;    
        *epinicio = (*epinicio)->prox;
        p1->prox->ant = p1->ant;
        p1->ant->prox = p1->prox;
        free (p1);
       }
    }         
    if ((*epinicio != NULL) && ((*epinicio)->prox != *epinicio)) {
      p1 = (*epinicio)->prox;
      while (p1 != *epinicio) 
        if (p1->dado == chave) {
          p2 = *epinicio;
          while (p2->prox != p1)
            p2 = p2->prox;
          p2->prox = p1->prox;
          p1->prox->ant = p2;
          free (p1);
          p1 = p2->prox;  
          }  
        else    
          p1 = p1->prox;
    }
  }       
}

//--------------------------------------------
void DestroiListaFD(listaD **epinicio){
  listaD *p1;
  
  if (*epinicio != NULL) {
    p1 = (*epinicio)->prox;
    while (p1 != *epinicio) {
      (*epinicio)->prox = p1->prox;
      free (p1);
      p1 = (*epinicio)->prox;
    }
    free (*epinicio);
    *epinicio = NULL;
  }
}  

//--------------------------------------------
main () {
  listaD *pini;
  char c;
// ConstroiListaFD1 (&pini);
// PercorreListaFD (pini);
    
 ConstroiListaFD(&pini);
 PercorreListaFD (pini);
     
/* printf ("entre com dado a ser procurado \n");
 fflush(stdin);
 scanf ("%c" , &c);
 paux = ProcuraListaFD (pini,c);
 if (paux == NULL)
   printf("elemento ausente \n");
 else
   printf("elemento: %c \n", c);  */

printf ("entre com dado a ser inserido\n");
 fflush(stdin);
 scanf ("%c" , &c);
 InsereListaFD (&pini, c);  
 PercorreListaFD(pini); 
/*
  int i;
  for (i=1; i !=6; i++) {     
     printf ("entre com dado a ser removido\n");
     fflush(stdin);
     scanf ("%c" , &c);
     RemoveListaFD (&pini, c);
     PercorreListaFD (pini);
     } 
 */ 
/*  DestroiListaFD(&pini);
  PercorreListaFD (pini); */ 
     
  system("pause");
}
     
     
     
     
     
     
     
     
     
