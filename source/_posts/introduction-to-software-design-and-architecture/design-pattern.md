# Design Pattern

## Creational and Structural Design Patterns

### Singleton Pattern

* One object of a class.
* Globally accessible within the program.

```java
Public class ExampleSingleton { // lazy construction
    // the class variable is null if no instance is
    // instantiated
    Private static ExampleSingleton uniqueInstance = null;
    Private ExampleSingleton() {
        …
    }

    // lazy construction of the instance
    Public static ExampleSingleton getInstance() {
        if (uniqueInstance == null) {
            uniqueInstance = new ExampleSingleton();
        }
        Return uniqueInstance;
    }
    …
}
```

### Factory Method Pattern

```java
public class KnifeFactory {
    public Knife createKnife(String knifeType) {
        Knife knife = null;
        
        // create Knife object
        If (knifeType.equals("steak")) {
            knife = new SteakKnife();
        } else if (knifeType.equals("chefs")) {
            knife = new ChefsKnife();
        }
        
        return knife;
    }
}
```

### Facade /fə'sɑ:d/ Design Pattern

* A facade simply acts as a point of entry into the subsystem
* Wrapper class that encapsulates a subsystem in order to hide the subsystem's complexity
* A facade class can be used to wrap all the interfaces and classes for a subsystem

###  Adapter Pattern

* Facilitates communication between two existing systems by providing a compatible interface.

###  Composite Pattern (Polymorphism)

* Enforcing polymorphism across each class through implementing an interface (or inheriting from a superclass).

* ![-w592](https://i.imgur.com/Xhymsyn.jpg)

### Proxy Pattern

* ![-w685](https://i.imgur.com/95TrYe3.jpg)
* In this example, class `OderFulfillment` is the proxy class, which implement interface `IOrder`, and send the requests to `Warehouse`.

### Decorator Pattern

* Add additional functions to the original classes
* Serves as the abstract superclass of concrete decorator classes that will each provide an increment of behaviour
* ![-w588](https://i.imgur.com/JoZnT6O.jpg)

## Behavioural Design Patterns

* Focus on how independent objects work towards a common goal

### Template Method Pattern

* ![-w574](https://i.imgur.com/lrUfvaH.jpg)

### Chain of Responsibility Pattern

* Like `switch` and `try/catch` block
* ![-w514](https://i.imgur.com/mMWOELQ.jpg)

### State Pattern

* Change the behaviour of an object based on the state that it's in at run-time. 
* ![-w635](https://i.imgur.com/dvRauOx.jpg)

### Command Pattern

* ![-w533](https://i.imgur.com/xxQcOIl.jpg)

### Observer Pattern

* ![-w270](https://i.imgur.com/jrftBty.jpg)

* ![-w621](https://i.imgur.com/TRO9yzx.jpg)

## Design Principles

### MVC Pattern

* Basic Model-View-Control Pattern.

### Open/Closed Principle

* Consider a class as being `closed` to editing once it has been:
    * Tested to be functioning properly
    * All the attributes and behaviours are encapsulated
    * Proven to be stable within your system

### Dependency Inversion Principle

* The principle states that high level modules should be depend on high level generalizations, and not on low level details.
* The client classes should depend on an interface or abstract class instead of referring to concrete resources.
* ![-w617](https://i.imgur.com/BEws7g1.jpg)

### Composing Objects Principle

* This principle states that classes should achieve code reuse through **aggregation** rather that inheritance to reduce coupling.
* Inheritance should be only used to extend classes.

### Interface Segregation Principle

* The Interface Segregation Principle states that **a class should bot be forced to depend on methods it does not use**. This means that any classes that implement an interface, should not have "dummy" implementations of any methods defined in the interface. Instead, you should **split large interfaces into smaller generalizations**.
* ![-w573](https://i.imgur.com/mVplPsi.jpg)

### Principle of Least Knowledge

* **Classes should know about and interact with as few other classes as possible.**
* A method, M, of an object should only call other methods if they are:
    1. Encapsulated within the same object.
    2. Encapsulated within an object that is in the parameters of M.
    3. Encapsulated within an object that is instantiated inside the M.
    4. Encapsulated within an object that is referenced in an instance variable of the class for M.

## UML

* https://www.uml-diagrams.org/index-examples.html
* https://tallyfy.com/uml-diagram/

## Words

* encapsulate vt. 压缩；将…装入胶囊；将…封进内部；概述 vi. 形成胶囊
* delegate ['deliɡət, -ɡeit, 'deliɡeit] vt. 委派…为代表 n. 代表
* stimulate ['stimjuleit] vt. 刺激；鼓舞，激励 vi. 起刺激作用；起促进作用
* generalization [,dʒenərəlai'zeiʃən, -li'z-] n. 概括；普遍化；一般化 接口化
* abstraction 抽象化
* polymorphism [,pɔli'mɔ:fizm] n. 多态性；多形性；同质多晶
* segregation [,seɡri'ɡeiʃən] n. 隔离，分离；种族隔离
