class Pracklr:
    def avail_lx_prog():
        avail_dm = r"""
        1. disp_r_ver()
        
        2. data_types()
        
        3. operators()
        
        4. conditional()
        
        5. looping()
        
        6. vectors()
        
        7. matrix()
        
        8. factors()
        
        9. data_frame()
        
        10. list_prog()
        
        11. class_deision_tree()
        
        12. class_rand_forest()
        
        13. class_naive()
        
        14. clust_kmeans()
        
        15. clust_kmedoids()
        
        16. clust_clara()
        
        17. clust_hier()
        
        18. association()
        
        """
        return avail_dm
    def disp_r_ver():
        od = r"""
	name = readline(prompt ="Input your name:");
	age = readline(prompt="Input your age: ");
	address = readline(prompt="Input your address:")
	print(paste("My name is ",name, "and I am ",age, "years old. I am from", address))
	print(R.version.string)
        
        """
        return od
        
    def data_types():
        ten = r""" 
	# integer data type
	x = as.integer(5)
	print(class(x))
	print(typeof(x))
	y = 5L
	print(class(y))
	print(typeof(y))
	# logical data type
	a = 4
	b = 3
	c = a > b
	print(c)
	print(class(c))
	print(typeof(c))
	#complex data type
	d= 4 + 3i
	print(class(d))
	print(typeof(d))
	#character data type
	char = "R programming"
	print(class(char))
	print(typeof(char))
	# convert data type of an object to another
	print(as.numeric(TRUE))
	print(as.complex(3L))
	print(as.logical(10.5))
	print(as.character(1+2i))
        """
        return ten
    def operators():
       ma = r"""
	x= readline(prompt="Enter the value for x:");
	y= readline(prompt="Enter the value for y:");
	x= as.integer(x)
	y= as.integer(y)
	print(x+y)
	print(x-y)
	print(x*y)
	print(x/y)
	print(x%%y)
	print(x%/%y)
	print(x^y)
	print(x:y)
	print(y %in% x)
       """
       return ma
       
    def conditional():
       ser = r""" 
	week= as.integer(readline(prompt = "enter a number:"))
	if(week == 1){
	print("Monday")
	}else if(week == 2){
	print("Tuesday")
	}else if(week == 3){
	print("Wednesday")
	}else if(week == 4){
	print("Thursday")
	}else if(week == 5){
	print("Friday")
	}else if(week == 6){
	print("Saturday")
	}else if(week == 7){
	print("Sunday")
	}else{
	print("Invalid Input! please enter week number between 1-7")
	}
       """
       return ser
    def looping():
        cp = r""" 
	num= as.integer(readline(prompt = "Enter a number:"))
	factorial= 1
	if(num<0){
	print("Sorry, factorial does not exist for negative numbers")
	}else if(num==0){
	print("The factorial of 0 is 1")
	}else{
	for (i in 1:num){
	factorial= factorial * i
	}
	print(paste("The factorial of ",num," is ",factorial))
	}
        """
        return cp
        
    def vectors():
          sc = r""" 
		v=c(0,10,40,30,30,20,50,50,90,80,60)
		print("Original vector:")
		print(v)
		ctr=sum(v>10 & v<80)
		print("Number of vector values between 10 and 80:")
		print(ctr)
		v[3]<- 11
		print("Modified vector")
		print(v)
		print("unique elements of the said vector: ")
		print(unique(v))
		print(" sorted vector")
		print(sort(v))

         """
          return sc
         
    def matrix():
          ex_fam = r""" 
		x= matrix(1:12, ncol=3)
		y= matrix(13:24, ncol=3)
		print("Matrix-1")
		print(x)
		print("Size of matrix x")
		print(dim(x))
		print("Matrix-2")
		print(y)
		print("Size of matrix y")
		print(dim(y))
		result=rbind(x,y)
		print("After concatenating two given matrices:")
		print(result)
		print("size of matrix after concatenation")
		print(dim(rbind(x,y)))
		sum=x+y
		print("Result of addition ")
		print(sum)
		sub=x-y
		print("Result of subtraction ")
		print(sub)
		mul=x*y
		print("Resukt of multiplication")
		print(mul)
		div=x/y
		print("Result of division")
		print(div)
          """
          return ex_fam   
    def factors():
          cld = r""" 
		mons_v =c("March","April","January", "November ","January",
		"September", "October", "September", "November", "August", "February",
		"January", "November", "November", "February", "May", "August", "February",
		"July", "December", "August", "August", "September", "November",
		"September","February", "April")
		print("Original vector:")
		print(mons_v)
		f = factor (mons_v)
		print("Ordered factors of the said vector:")
		print(f)
		print(table(f))
          """
          return cld
    
    def data_frame():
          waitf = r"""  
		a=c(10,20,10,10,40,50,20,30)
		b=c(10,30,10,20,0,50,30,30)
		print("Original data frame:")
		ab=data.frame(a,b)
		print(ab)
		print("Duplicate elements of the said data frame:")
		print(duplicated(ab))
		print("Unique rows of the said data frame:")
		print(unique(ab))
		d=c("IT","OPERATIONS","IT","HR","FINANCE","CS","MANAGER","DEPT")
		abd=data.frame(a,b,d)
		print(abd)
		new=abd[-c(2),-c(2)]
		print(new)
		print("Before removing second row and column length: ")
		print(length(abd))
		print("After removing second row and column length: ")
		print(length(new))

          
          """
          return waitf      
    def list_prog():
          sig_lam = r"""           
		list_data=list(c("Red","Green","Black"),matrix(c(1,3,5,7,9,11),nrow=2),
		list("Python","PHP","Java"))
		print("List:")
		print(list_data)
		names(list_data)=c("Colours","Odd numbers","Language(s)")
		print(list_data)
		list1=list(1,2,3)
		print(list1)
		merged.list=c(list_data,list1)
		print(merged.list)
		print("Remove the second element of the list:")
		list_data[2]=NULL
		print("New list:")
		print(list_data)
		print("1st element")
		print(list_data[1])
		print("2nd element")
		print(list_data[2])
          """
          return sig_lam   
    def class_deision_tree():
          sig_int = r""" 
		install.packages("rpart")

		install.packages("rpart.plot")
		library(rpart)
		library(rpart.plot)
		data(iris)
		set.seed(123)
		train_index <- sample(nrow(iris), 0.7 * nrow(iris))
		train_data <- iris[train_index, ]
		test_data <- iris[-train_index, ]
		model <- rpart(Species ~ ., data = train_data, method = "class")
		rpart.plot(model)
		predictions <- predict(model, test_data[, -5], type = "class")
		accuracy <- sum(predictions == test_data[, 5]) / nrow(test_data)
		accuracy
          """
          return sig_int
    def class_rand_forest():
          pipe_po_pc = r"""
		install.packages("caTools") # For sampling the dataset
		install.packages("randomForest") # For implementing random forest algorithm
		library(caTools)
		library(randomForest)
		split <- sample.split(iris, SplitRatio = 0.7)
		split
		train <- subset(iris, split == "TRUE")
		test <- subset(iris, split == "FALSE")
		set.seed(120) # Setting seed
		classifier_RF = randomForest(x = train[-5],
		y = train$Species,
		ntree = 500)
		classifier_RF
		y_pred = predict(classifier_RF, newdata = test[-5])
		confusion_mtx = table(test[, 5], y_pred)
		confusion_mtx
		plot(classifier_RF)
		importance(classifier_RF)
		varImpPlot(classifier_RF)
          """
          return pipe_po_pc
          
    def class_naive():
          rd_pip = r"""
		install.packages("e1071")

		install.packages("ggplot2")
		library(e1071)
		library(ggplot2)
		data(iris)
		set.seed(123)
		train_index <- sample(nrow(iris), 0.8 * nrow(iris))
		train_data <- iris[train_index, ]
		test_data <- iris[-train_index, ]
		nb_model <- naiveBayes(Species ~ ., data = train_data)
		pred <- predict(nb_model, test_data, type = "class")
		conf_mat <- table(pred, test_data$Species)
		ggplot(data.frame(expand.grid(Prediction = rownames(conf_mat), Actual =
		colnames(conf_mat)),
		Count = as.vector(conf_mat)),
		aes(x = Prediction, y = Actual)) +
		geom_tile(aes(fill = Count), colour = "white") +
		geom_text(aes(label = Count)) +
		scale_fill_gradient(low = "white", high = "steelblue") +
		theme_minimal() +
		theme(axis.text = element_text(size = 20),
		axis.title = element_text(size = 20),
		legend.text = element_text(size = 20),
		legend.title = element_text(size = 20)) +
		labs(title = "Naive Bayes Confusion Matrix for Iris Dataset",
		x = "Predicted Species",
		y = "Actual Species")
          """ 
          return rd_pip  
          
    def clust_kmeans():
          cal_ser = r""" 
		install.packages("factoextra")

		install.packages("cluster")
		library(factoextra)
		library(cluster)
		#load data
		df <- USArrests
		#remove rows with missing values
		df <- na.omit(df)
		#scale each variable to have a mean of 0 and sd of 1
		df <- scale(df)
		#view first six rows of dataset
		head(df)
		#create a plot of the number of clusters vs. the total within sum of squares
		fviz_nbclust(df, kmeans, method = "wss")
		#calculate gap statistic based on number of clusters
		gap_stat <- clusGap(df,
		FUN = kmeans,
		nstart = 25,
		K.max = 10,
		B = 50)
		#plot number of clusters vs. gap statistic
		fviz_gap_stat(gap_stat)
		#make thiexample reproducible
		set.seed(1)
		#perform k-means clustering with k = 4 clusters
		km <- kmeans(df, centers = 4, nstart = 25)
		km
		fviz_cluster(km, data = df)
		aggregate(USArrests, by=list(cluster=km$cluster), mean)#add cluster assigment to original
		data
		final_data <- cbind(USArrests, cluster = km$cluster)
		head(final_data)
          """
          return cal_ser 
    def clust_kmedoids():
          prod = r""" 
          
        install.packages("cluster")
		library(factoextra)
		library(cluster)
		df <- USArrests
		df <- na.omit(df)
		head(df)
		fviz_nbclust(df, pam, method = "wss")
		gap_stat <- clusGap(df, FUN = pam, K.max = 10, B = 50)
		fviz_gap_stat(gap_stat)
		set.seed(1)
		kmed <- pam(df, k = 4)
		kmed
		fviz_cluster(kmed, data = df)
		final_data <- cbind(USArrests, cluster = kmed$cluster)
		head(final_data)
          """
          return prod
    def clust_clara(): 
         msg_q = r""" 
        # Load the USArrests dataset
		data("USArrests")
		# Scale the data
		scaled_data <- scale(USArrests)
		# Cluster the data using the CLARA algorithm
		library(cluster)
		set.seed(123)
		clara_results <- clara(scaled_data, 3)
		#Display the data
		print(clara_results)
		# Install and load the factoextra package
		install.packages("factoextra")
		library(factoextra)
		# Plot the clusters
		fviz_cluster(clara_results, data = scaled_data, palette = "jco", geom = "point")
		# Plot the silhouette widths
		sil_width <- silhouette(clara_results$clustering, dist(scaled_data))
		fviz_silhouette(sil_width)
         """      
         return msg_q
    def clust_hier():
         hier = r"""
        Error Occured

		library(factoextra)
		library(cluster)
		#load data
		df <- USArrests
		#remove rows with missing values
		df <- na.omit(df)
		#scale each variable to have a mean of 0 and sd of 1
		df <- scale(df)
		#view first six rows of dataset
		head(df)
		#define linkage methods
		m <- c( "average", "single", "complete", "ward")
		names(m) <- c( "average", "single", "complete", "ward")
		#function to compute agglomerative coefficient
		ac <- function(x) {
		agnes(df, method = x)$ac
		}
		#calculate agglomerative coefficient for each clustering linkage method
		sapply(m, ac)
		#perform hierarchical clustering using Ward's minimum variance
		clust <- agnes(df, method = "ward")
		#produce dendrogram
		pltree(clust, cex = 0.6, hang = -1, main = "Dendrogram")
		#calculate gap statistic for each number of clusters (up to 10 clusters)gap_stat <- clusGap(df, FUN = hcut, nstart = 25, K.max = 10, B = 50)
		#produce plot of clusters vs. gap statistic
		fviz_gap_stat(gap_stat)
		#compute distance matrix
		d <- dist(df, method = "euclidean")
		#perform hierarchical clustering using Ward's method
		final_clust <- hclust(d, method = "ward.D2" )
		#cut the dendrogram into 4 clusters
		groups <- cutree(final_clust, k=4)
		#find number of observations in each cluster
		table(groups)
		#append cluster labels to original data
		final_data <- cbind(USArrests, cluster = groups)
		#display first six rows of final data
		head(final_data)
		#find mean values for each cluster
		aggregate(final_data, by=list(cluster=final_data$cluster), mean)
		table(sub_grp)
		USArrests %>%
		head
		plot(hc5, cex = 0.6)
		rect.hclust(hc5, k = 4, border = 2:5)
		fviz_cluster(list(data = df, cluster = sub_grp))
		 """
         return hier
    def association():
         asso = r"""
         # Installing Packages
		install.packages("arules")
		install.packages("arulesViz")

		# Loading package
		library(arules)
		library(arulesViz)
		data("Groceries")

		# Fitting model
		# Training Apriori on the dataset
		set.seed = 220 # Setting seed
		associa_rules = apriori(data = Groceries,parameter = list(support = 0.004,confidence = 0.2))

		# Plot
		itemFrequencyPlot(Groceries, topN = 10)

		# Visualising the results
		inspect(sort(associa_rules, by = 'lift')[1:10])
		plot(associa_rules, method = "graph",
		measure = "confidence", shading = "lift")
		 """
         return asso 
		 
		 
         
