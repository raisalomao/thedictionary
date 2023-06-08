import java.util.Scanner;

class Main {
    public static void main(String[] args){
        String nome;
        int idade;
        float altura;
        Scanner entrada = new Scanner (System.in);

        System.out.print("Digite seu nome: ");
        nome = entrada.nextLine();
        System.out.print("Digite sua idade: ");
        idade = entrada.nextInt();
        System.out.print("Digite sua altura: ");
        altura =  entrada.nextFloat();

        System.out.println("\n" + nome + " tem " + idade + " anos de idade " + altura + " metros de altura. ");
        entrada.close();

    }
}