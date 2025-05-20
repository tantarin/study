from models import Question

SPRING_CARDS = [
    Question(
        text="Основы Spring Framework",
        theory="""Spring Framework - это популярный фреймворк для разработки Java-приложений:

1. Основные модули:
- Spring Core: основа фреймворка
- Spring Context: управление зависимостями
- Spring Beans: управление жизненным циклом
- Spring AOP: аспектно-ориентированное программирование

2. IoC (Inversion of Control):
- Инверсия управления
- Внедрение зависимостей
- Контейнер Spring
- Аннотации @Autowired, @Component

3. Spring Boot:
- Автоконфигурация
- Встроенный сервер
- Starter-зависимости
- Actuator

4. Spring Data:
- Работа с БД
- JPA/Hibernate
- Репозитории
- Транзакции""",
        theory_summary="Spring Framework предоставляет комплексное решение для разработки Java-приложений с поддержкой IoC и DI.",
        correct_answer="",
        options=[],
        explanation="""Давайте разберем основные концепции Spring на примерах:

1. Создание простого Spring Boot приложения:
```java
@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}

@Service
public class UserService {
    private final UserRepository userRepository;
    
    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

2. Работа с репозиториями:
```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByEmail(String email);
    
    @Query("SELECT u FROM User u WHERE u.age > :age")
    List<User> findUsersOlderThan(@Param("age") int age);
}

@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String email;
    
    // Геттеры и сеттеры
}
```

3. Конфигурация через application.properties:
```properties
# Настройки базы данных
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=user
spring.datasource.password=password

# Настройки JPA
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect

# Настройки сервера
server.port=8080
```

4. Создание REST контроллера:
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;
    
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(userService.save(user));
    }
}
```

5. Обработка исключений:
```java
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage()
        );
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
}
```

Практические советы:
1. Используйте конструктор для внедрения зависимостей
2. Применяйте интерфейсы для лучшей тестируемости
3. Используйте Spring Boot для быстрого старта
4. Следуйте принципам REST при создании API
5. Обрабатывайте исключения глобально""",
        points=0
    ),
    Question(
        text="Spring Security",
        theory="""Spring Security - фреймворк для обеспечения безопасности приложений:

1. Основные концепции:
- Аутентификация
- Авторизация
- Защита от атак
- Управление сессиями

2. Механизмы аутентификации:
- Form-based
- Basic Auth
- OAuth2
- JWT

3. Авторизация:
- Роли и права
- Аннотации @Secured
- Методы hasRole()
- SpEL выражения

4. Защита:
- CSRF
- XSS
- SQL Injection
- CORS""",
        theory_summary="Spring Security предоставляет комплексное решение для обеспечения безопасности приложений.",
        correct_answer="",
        options=[],
        explanation="""Давайте разберем Spring Security на примерах:

1. Базовая конфигурация:
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .antMatchers("/public/**").permitAll()
                .antMatchers("/api/**").authenticated()
                .antMatchers("/admin/**").hasRole("ADMIN")
            .and()
            .formLogin()
                .loginPage("/login")
                .permitAll()
            .and()
            .logout()
                .permitAll();
    }
}
```

2. JWT аутентификация:
```java
@Component
public class JwtTokenProvider {
    @Value("${jwt.secret}")
    private String jwtSecret;
    
    public String generateToken(Authentication authentication) {
        UserDetails userDetails = (UserDetails) authentication.getPrincipal();
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + 86400000); // 24 часа
        
        return Jwts.builder()
                .setSubject(userDetails.getUsername())
                .setIssuedAt(now)
                .setExpiration(expiryDate)
                .signWith(SignatureAlgorithm.HS512, jwtSecret)
                .compact();
    }
    
    public String getUsernameFromToken(String token) {
        Claims claims = Jwts.parser()
                .setSigningKey(jwtSecret)
                .parseClaimsJws(token)
                .getBody();
        
        return claims.getSubject();
    }
}
```

3. Защита эндпоинтов:
```java
@RestController
@RequestMapping("/api")
public class UserController {
    
    @GetMapping("/profile")
    @PreAuthorize("isAuthenticated()")
    public UserProfile getProfile() {
        // Получение профиля пользователя
    }
    
    @PostMapping("/admin/users")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<User> createUser(@RequestBody User user) {
        // Создание пользователя
    }
}
```

4. Кастомный UserDetailsService:
```java
@Service
public class CustomUserDetailsService implements UserDetailsService {
    
    private final UserRepository userRepository;
    
    @Autowired
    public CustomUserDetailsService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userRepository.findByUsername(username)
            .orElseThrow(() -> new UsernameNotFoundException("User not found"));
            
        return new org.springframework.security.core.userdetails.User(
            user.getUsername(),
            user.getPassword(),
            user.getRoles().stream()
                .map(role -> new SimpleGrantedAuthority(role.getName()))
                .collect(Collectors.toList())
        );
    }
}
```

5. CORS конфигурация:
```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("https://trusted-domain.com")
            .allowedMethods("GET", "POST", "PUT", "DELETE")
            .allowedHeaders("*")
            .allowCredentials(true)
            .maxAge(3600);
    }
}
```

Практические советы:
1. Всегда используйте HTTPS в продакшене
2. Храните секреты в защищенном месте
3. Регулярно обновляйте зависимости
4. Используйте принцип наименьших привилегий
5. Логируйте все попытки доступа""",
        points=0
    )
] 