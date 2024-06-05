## 
连接GoDoc的
类型是包的核心。它包裹着一个原始的 网络连接，用于向 Kafka 服务器公开低级 API。Connkafka-go

下面是一些示例，显示了连接对象的典型用法：

// to produce messages
topic := "my-topic"
partition := 0

conn, err := kafka.DialLeader(context.Background(), "tcp", "localhost:9092", topic, partition)
if err != nil {
    log.Fatal("failed to dial leader:", err)
}

conn.SetWriteDeadline(time.Now().Add(10*time.Second))
_, err = conn.WriteMessages(
    kafka.Message{Value: []byte("one!")},
    kafka.Message{Value: []byte("two!")},
    kafka.Message{Value: []byte("three!")},
)
if err != nil {
    log.Fatal("failed to write messages:", err)
}

if err := conn.Close(); err != nil {
    log.Fatal("failed to close writer:", err)
}
// to consume messages
topic := "my-topic"
partition := 0

conn, err := kafka.DialLeader(context.Background(), "tcp", "localhost:9092", topic, partition)
if err != nil {
    log.Fatal("failed to dial leader:", err)
}

conn.SetReadDeadline(time.Now().Add(10*time.Second))
batch := conn.ReadBatch(10e3, 1e6) // fetch 10KB min, 1MB max

b := make([]byte, 10e3) // 10KB max per message
for {
    n, err := batch.Read(b)
    if err != nil {
        break
    }
    fmt.Println(string(b[:n]))
}

if err := batch.Close(); err != nil {
    log.Fatal("failed to close batch:", err)
}

if err := conn.Close(); err != nil {
    log.Fatal("failed to close connection:", err)
}
创建主题
默认情况下，kafka 在 bitnami/kafka kafka docker 映像中具有 （ ）。如果此值设置为，则将创建主题作为如下的副作用：auto.create.topics.enable='true'KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE='true''true'kafka.DialLeader

// to create topics when auto.create.topics.enable='true'
conn, err := kafka.DialLeader(context.Background(), "tcp", "localhost:9092", "my-topic", 0)
if err != nil {
    panic(err.Error())
}
如果那样的话，您将需要像这样显式创建主题：auto.create.topics.enable='false'

// to create topics when auto.create.topics.enable='false'
topic := "my-topic"

conn, err := kafka.Dial("tcp", "localhost:9092")
if err != nil {
    panic(err.Error())
}
defer conn.Close()

controller, err := conn.Controller()
if err != nil {
    panic(err.Error())
}
var controllerConn *kafka.Conn
controllerConn, err = kafka.Dial("tcp", net.JoinHostPort(controller.Host, strconv.Itoa(controller.Port)))
if err != nil {
    panic(err.Error())
}
defer controllerConn.Close()


topicConfigs := []kafka.TopicConfig{
    {
        Topic:             topic,
        NumPartitions:     1,
        ReplicationFactor: 1,
    },
}

err = controllerConn.CreateTopics(topicConfigs...)
if err != nil {
    panic(err.Error())
}
通过非领导者连接连接到领导者
// to connect to the kafka leader via an existing non-leader connection rather than using DialLeader
conn, err := kafka.Dial("tcp", "localhost:9092")
if err != nil {
    panic(err.Error())
}
defer conn.Close()
controller, err := conn.Controller()
if err != nil {
    panic(err.Error())
}
var connLeader *kafka.Conn
connLeader, err = kafka.Dial("tcp", net.JoinHostPort(controller.Host, strconv.Itoa(controller.Port)))
if err != nil {
    panic(err.Error())
}
defer connLeader.Close()
列出主题
conn, err := kafka.Dial("tcp", "localhost:9092")
if err != nil {
    panic(err.Error())
}
defer conn.Close()

partitions, err := conn.ReadPartitions()
if err != nil {
    panic(err.Error())
}

m := map[string]struct{}{}

for _, p := range partitions {
    m[p.Topic] = struct{}{}
}
for k := range m {
    fmt.Println(k)
}
因为它是低级的，所以该类型被证明是一个很好的构建块 对于更高级别的抽象，例如ConnReader

读者GoDoc的
A 是包暴露的另一个概念，它旨在 使实现从单个消费的典型用例更简单 topic-partition 对。 A 还自动处理重新连接和偏移管理，以及 公开一个 API，该 API 支持使用 Go 进行异步取消和超时 上下文。Readerkafka-goReader

请注意，在进程退出时调用 a 非常重要。 Kafka 服务器需要一个优雅的断开连接来阻止它继续 尝试向连接的客户端发送消息。给定的示例不会 如果进程使用 SIGINT（在 shell 中按 ctrl-c 键）终止，则调用 SIGTERM（如 docker stop 或 kubernetes 重启）。这可能会导致 当同一主题的新读者连接时延迟（例如，新进程已启动） 或正在运行的新容器）。使用处理程序关闭读取器 进程关闭。Close()ReaderClose()signal.Notify

// make a new reader that consumes from topic-A, partition 0, at offset 42
r := kafka.NewReader(kafka.ReaderConfig{
    Brokers:   []string{"localhost:9092","localhost:9093", "localhost:9094"},
    Topic:     "topic-A",
    Partition: 0,
    MaxBytes:  10e6, // 10MB
})
r.SetOffset(42)

for {
    m, err := r.ReadMessage(context.Background())
    if err != nil {
        break
    }
    fmt.Printf("message at offset %d: %s = %s\n", m.Offset, string(m.Key), string(m.Value))
}

if err := r.Close(); err != nil {
    log.Fatal("failed to close reader:", err)
}
消费者群体
kafka-go还支持 Kafka 使用者组，包括代理管理的偏移量。 要启用使用者组，只需在 ReaderConfig 中指定 GroupID。

使用使用者组时，ReadMessage 会自动提交偏移量。

// make a new reader that consumes from topic-A
r := kafka.NewReader(kafka.ReaderConfig{
    Brokers:   []string{"localhost:9092", "localhost:9093", "localhost:9094"},
    GroupID:   "consumer-group-id",
    Topic:     "topic-A",
    MaxBytes:  10e6, // 10MB
})

for {
    m, err := r.ReadMessage(context.Background())
    if err != nil {
        break
    }
    fmt.Printf("message at topic/partition/offset %v/%v/%v: %s = %s\n", m.Topic, m.Partition, m.Offset, string(m.Key), string(m.Value))
}

if err := r.Close(); err != nil {
    log.Fatal("failed to close reader:", err)
}
使用使用者组时存在许多限制：

(*Reader).SetOffset设置 GroupID 时将返回错误
(*Reader).Offset设置 GroupID 时将始终返回-1
(*Reader).Lag设置 GroupID 时将始终返回-1
(*Reader).ReadLag设置 GroupID 时将返回错误
(*Reader).Stats将返回设置 GroupID 时的分区-1
显式提交
kafka-go还支持显式提交。而不是调用， call 后跟 .ReadMessageFetchMessageCommitMessages

ctx := context.Background()
for {
    m, err := r.FetchMessage(ctx)
    if err != nil {
        break
    }
    fmt.Printf("message at topic/partition/offset %v/%v/%v: %s = %s\n", m.Topic, m.Partition, m.Offset, string(m.Key), string(m.Value))
    if err := r.CommitMessages(ctx, m); err != nil {
        log.Fatal("failed to commit messages:", err)
    }
}
在消费者组中提交消息时，偏移量最高的消息 对于给定的主题/分区，确定 那个分区。例如，如果单个偏移量为 1、2 和 3 的消息 通过调用 to 检索分区，使用消息偏移量 3 进行调用也会导致在偏移量 1 处提交消息 和 2 表示该分区。FetchMessageCommitMessages

管理提交
默认情况下，CommitMessages 将同步提交偏移量到 Kafka。为 改进了性能，您可以定期将偏移量提交到 Kafka 通过在 ReaderConfig 上设置 CommitInterval。

// make a new reader that consumes from topic-A
r := kafka.NewReader(kafka.ReaderConfig{
    Brokers:        []string{"localhost:9092", "localhost:9093", "localhost:9094"},
    GroupID:        "consumer-group-id",
    Topic:          "topic-A",
    MaxBytes:       10e6, // 10MB
    CommitInterval: time.Second, // flushes commits to Kafka every second
})
作家GoDoc的
为了向 Kafka 生成消息，程序可以使用低级 API，但 该软件包还提供了更合适的更高级别的类型 在大多数情况下使用，因为它提供了附加功能：ConnWriter

出错时自动重试和重新连接。
在可用分区之间配置消息分布。
将消息同步或异步写入 Kafka。
使用上下文进行异步取消。
刷新挂起的消息，以支持正常关机。
在发布消息之前创建缺少的主题。注意！这是该版本之前的默认行为。v0.4.30
// make a writer that produces to topic-A, using the least-bytes distribution
w := &kafka.Writer{
	Addr:     kafka.TCP("localhost:9092", "localhost:9093", "localhost:9094"),
	Topic:   "topic-A",
	Balancer: &kafka.LeastBytes{},
}

err := w.WriteMessages(context.Background(),
	kafka.Message{
		Key:   []byte("Key-A"),
		Value: []byte("Hello World!"),
	},
	kafka.Message{
		Key:   []byte("Key-B"),
		Value: []byte("One!"),
	},
	kafka.Message{
		Key:   []byte("Key-C"),
		Value: []byte("Two!"),
	},
)
if err != nil {
    log.Fatal("failed to write messages:", err)
}

if err := w.Close(); err != nil {
    log.Fatal("failed to close writer:", err)
}
发布前缺少主题创建
// Make a writer that publishes messages to topic-A.
// The topic will be created if it is missing.
w := &Writer{
    Addr:                   kafka.TCP("localhost:9092", "localhost:9093", "localhost:9094"),
    Topic:                  "topic-A",
    AllowAutoTopicCreation: true,
}

messages := []kafka.Message{
    {
        Key:   []byte("Key-A"),
        Value: []byte("Hello World!"),
    },
    {
        Key:   []byte("Key-B"),
        Value: []byte("One!"),
    },
    {
        Key:   []byte("Key-C"),
        Value: []byte("Two!"),
    },
}

var err error
const retries = 3
for i := 0; i < retries; i++ {
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    
    // attempt to create topic prior to publishing the message
    err = w.WriteMessages(ctx, messages...)
    if errors.Is(err, kafka.LeaderNotAvailable) || errors.Is(err, context.DeadlineExceeded) {
        time.Sleep(time.Millisecond * 250)
        continue
    }

    if err != nil {
        log.Fatalf("unexpected error %v", err)
    }
    break
}

if err := w.Close(); err != nil {
    log.Fatal("failed to close writer:", err)
}
写入多个主题
通常，用于初始化单主题编写器。 通过排除该特定配置，您可以定义 通过设置 .WriterConfig.TopicMessage.Topic

w := &kafka.Writer{
	Addr:     kafka.TCP("localhost:9092", "localhost:9093", "localhost:9094"),
    // NOTE: When Topic is not defined here, each Message must define it instead.
	Balancer: &kafka.LeastBytes{},
}

err := w.WriteMessages(context.Background(),
    // NOTE: Each Message has Topic defined, otherwise an error is returned.
	kafka.Message{
        Topic: "topic-A",
		Key:   []byte("Key-A"),
		Value: []byte("Hello World!"),
	},
	kafka.Message{
        Topic: "topic-B",
		Key:   []byte("Key-B"),
		Value: []byte("One!"),
	},
	kafka.Message{
        Topic: "topic-C",
		Key:   []byte("Key-C"),
		Value: []byte("Two!"),
	},
)
if err != nil {
    log.Fatal("failed to write messages:", err)
}

if err := w.Close(); err != nil {
    log.Fatal("failed to close writer:", err)
}
注意：这 2 种模式是互斥的，如果你设置 ， 您不得在消息上明确定义您是 写作。当您不为作者定义主题时，情况正好相反。 如果检测到此歧义，则将返回错误。Writer.TopicMessage.TopicWriter

与其他客户端的兼容性
萨拉马
如果您要从 Sarama 切换，并且需要/想要使用相同的算法进行消息分区，则可以使用 平衡器或平衡器：kafka.Hashkafka.ReferenceHash

kafka.Hash = sarama.NewHashPartitioner
kafka.ReferenceHash = sarama.NewReferenceHashPartitioner
和 均衡器会将消息路由到与两者相同的分区 前面提到的 Sarama 分区器会将它们路由到。kafka.Hashkafka.ReferenceHash

w := &kafka.Writer{
	Addr:     kafka.TCP("localhost:9092", "localhost:9093", "localhost:9094"),
	Topic:    "topic-A",
	Balancer: &kafka.Hash{},
}
librdkafka 和 confluent-kafka-go
使用平衡器获得与 librdkafka 相同的行为 默认分区策略。kafka.CRC32Balancerconsistent_random

w := &kafka.Writer{
	Addr:     kafka.TCP("localhost:9092", "localhost:9093", "localhost:9094"),
	Topic:    "topic-A",
	Balancer: kafka.CRC32Balancer{},
}
爪哇岛
使用平衡器获得与规范相同的行为 Java 客户端的缺省分区程序。注意：Java 类允许您直接指定 不允许的分区。kafka.Murmur2Balancer

w := &kafka.Writer{
	Addr:     kafka.TCP("localhost:9092", "localhost:9093", "localhost:9094"),
	Topic:    "topic-A",
	Balancer: kafka.Murmur2Balancer{},
}
压缩
可以通过设置以下字段来启用压缩：WriterCompression

w := &kafka.Writer{
	Addr:        kafka.TCP("localhost:9092", "localhost:9093", "localhost:9094"),
	Topic:       "topic-A",
	Compression: kafka.Snappy,
}
将通过确定消耗的消息是否被压缩 检查消息属性。但是，所有预期的包裹 必须导入编解码器才能正确加载。Reader

注意：在 0.4 之前的版本中，程序必须将压缩包导入到 安装编解码器并支持从 Kafka 读取压缩消息。这不是 压缩包的大小写和导入现在是无操作的。

TLS 支持
对于裸机 Conn 类型或在 Reader/Writer 配置中，您可以指定 TLS 支持的拨号器选项。如果 TLS 字段为 nil，则不会与 TLS 连接。注意：在未在 Conn/Reader/Writer 上配置 TLS 的情况下连接到启用了 TLS 的 Kafka 集群可能会以不透明的 io 显示。ErrUnexpectedEOF 错误。

连接
dialer := &kafka.Dialer{
    Timeout:   10 * time.Second,
    DualStack: true,
    TLS:       &tls.Config{...tls config...},
}

conn, err := dialer.DialContext(ctx, "tcp", "localhost:9093")
读者
dialer := &kafka.Dialer{
    Timeout:   10 * time.Second,
    DualStack: true,
    TLS:       &tls.Config{...tls config...},
}

r := kafka.NewReader(kafka.ReaderConfig{
    Brokers:        []string{"localhost:9092", "localhost:9093", "localhost:9094"},
    GroupID:        "consumer-group-id",
    Topic:          "topic-A",
    Dialer:         dialer,
})
作家
直接编写器创建

w := kafka.Writer{
    Addr: kafka.TCP("localhost:9092", "localhost:9093", "localhost:9094"), 
    Topic:   "topic-A",
    Balancer: &kafka.Hash{},
    Transport: &kafka.Transport{
        TLS: &tls.Config{},
      },
    }
用kafka.NewWriter

dialer := &kafka.Dialer{
    Timeout:   10 * time.Second,
    DualStack: true,
    TLS:       &tls.Config{...tls config...},
}

w := kafka.NewWriter(kafka.WriterConfig{
	Brokers: []string{"localhost:9092", "localhost:9093", "localhost:9094"},
	Topic:   "topic-A",
	Balancer: &kafka.Hash{},
	Dialer:   dialer,
})
请注意，和 已弃用，并将在将来的版本中删除。kafka.NewWriterkafka.WriterConfig

SASL 支持
您可以在 使用 SASL 身份验证上指定一个选项。可以直接用于打开一个，也可以通过各自的配置传递给一个或。如果字段为 ，则不会向 SASL 进行身份验证。DialerDialerConnReaderWriterSASLMechanismnil

SASL 身份验证类型
平原
mechanism := plain.Mechanism{
    Username: "username",
    Password: "password",
}
滚
mechanism, err := scram.Mechanism(scram.SHA512, "username", "password")
if err != nil {
    panic(err)
}
连接
mechanism, err := scram.Mechanism(scram.SHA512, "username", "password")
if err != nil {
    panic(err)
}

dialer := &kafka.Dialer{
    Timeout:       10 * time.Second,
    DualStack:     true,
    SASLMechanism: mechanism,
}

conn, err := dialer.DialContext(ctx, "tcp", "localhost:9093")
读者
mechanism, err := scram.Mechanism(scram.SHA512, "username", "password")
if err != nil {
    panic(err)
}

dialer := &kafka.Dialer{
    Timeout:       10 * time.Second,
    DualStack:     true,
    SASLMechanism: mechanism,
}

r := kafka.NewReader(kafka.ReaderConfig{
    Brokers:        []string{"localhost:9092","localhost:9093", "localhost:9094"},
    GroupID:        "consumer-group-id",
    Topic:          "topic-A",
    Dialer:         dialer,
})
作家
mechanism, err := scram.Mechanism(scram.SHA512, "username", "password")
if err != nil {
    panic(err)
}

// Transports are responsible for managing connection pools and other resources,
// it's generally best to create a few of these and share them across your
// application.
sharedTransport := &kafka.Transport{
    SASL: mechanism,
}

w := kafka.Writer{
	Addr:      kafka.TCP("localhost:9092", "localhost:9093", "localhost:9094"),
	Topic:     "topic-A",
	Balancer:  &kafka.Hash{},
	Transport: sharedTransport,
}
客户
mechanism, err := scram.Mechanism(scram.SHA512, "username", "password")
if err != nil {
    panic(err)
}

// Transports are responsible for managing connection pools and other resources,
// it's generally best to create a few of these and share them across your
// application.
sharedTransport := &kafka.Transport{
    SASL: mechanism,
}

client := &kafka.Client{
    Addr:      kafka.TCP("localhost:9092", "localhost:9093", "localhost:9094"),
    Timeout:   10 * time.Second,
    Transport: sharedTransport,
}
读取时间范围内的所有消息
startTime := time.Now().Add(-time.Hour)
endTime := time.Now()
batchSize := int(10e6) // 10MB

r := kafka.NewReader(kafka.ReaderConfig{
    Brokers:   []string{"localhost:9092", "localhost:9093", "localhost:9094"},
    Topic:     "my-topic1",
    Partition: 0,
    MaxBytes:  batchSize,
})

r.SetOffsetAt(context.Background(), startTime)

for {
    m, err := r.ReadMessage(context.Background())

    if err != nil {
        break
    }
    if m.Time.After(endTime) {
        break
    }
    // TODO: process message
    fmt.Printf("message at offset %d: %s = %s\n", m.Offset, string(m.Key), string(m.Value))
}

if err := r.Close(); err != nil {
    log.Fatal("failed to close reader:", err)
}
伐木
为了直观地了解 Reader/Writer 类型的操作，请在创建时配置记录器。

读者
func logf(msg string, a ...interface{}) {
	fmt.Printf(msg, a...)
	fmt.Println()
}

r := kafka.NewReader(kafka.ReaderConfig{
	Brokers:     []string{"localhost:9092", "localhost:9093", "localhost:9094"},
	Topic:       "my-topic1",
	Partition:   0,
	Logger:      kafka.LoggerFunc(logf),
	ErrorLogger: kafka.LoggerFunc(logf),
})
作家
func logf(msg string, a ...interface{}) {
	fmt.Printf(msg, a...)
	fmt.Println()
}

w := &kafka.Writer{
	Addr:        kafka.TCP("localhost:9092"),
	Topic:       "topic",
	Logger:      kafka.LoggerFunc(logf),
	ErrorLogger: kafka.LoggerFunc(logf),
}
测试
在以后的 Kafka 版本中，细微的行为变化导致一些历史测试中断，如果您针对 Kafka 2.3.1 或更高版本运行，则导出环境变量将跳过这些测试。KAFKA_SKIP_NETTEST=1

在 docker 中本地运行 Kafka

docker-compose up -d
运行测试

KAFKA_VERSION=2.3.1 \
  KAFKA_SKIP_NETTEST=1 \
  go test -race ./...
（或）清理缓存的测试结果并运行测试：

go clean -cache && make test
