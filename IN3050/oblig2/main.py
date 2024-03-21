from typing import Type
import numpy as np

from scaling import minmax_scaler, standard_scaler
from common import T_BINARY_TRAIN, T_BINARY_VAL, T_MULTI_TRAIN, T_MULTI_VAL, X_TRAIN, X_VAL, plot_decision_regions, plot_losses
from classifiers import Classifier, LinearRegressionClassifier, LogisticRegressionClassifier, MultiLogisticRegressionClassifier, accuracy


def test_classifier(
    x_train: np.ndarray,
    t_train: np.ndarray,
    x_val: np.ndarray,
    t_val: np.ndarray,
    decision_plot_path: str,
    losses_plot_path: str,
    classifier: Type[Classifier],
) -> None:
    best = 0.0
    best_epochs = None
    best_learning_rate = None
    best_tol = None
    best_c = classifier()

    # Since we're brute forcing so many different combinations of parameters, this may take a while
    # however in practice we would only have to run this once per dataset so thats fine. We could also
    # add more guesses for possible values here if we wanted.
    for epochs in range(100):
        for learning_rate in [0.0001, 0.001, 0.01, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]:
            for tol in [0.0001, 0.0005, 0.001, 0.01]:
                c = classifier()
                c.fit(x_train, t_train, x_val, t_val, learning_rate, epochs, tol)

                acc = accuracy(c.predict(x_val), t_val)

                if acc > best:
                    best = acc
                    best_epochs = epochs
                    best_learning_rate = learning_rate
                    best_tol = tol
                    best_c = c

    print(f"Best accuracy: {best}, with parameters: {best_epochs=}, {best_learning_rate=}, {best_tol=}")
    if best_c.val_losses.size > 0:
        print(f"Loss function change for value set: {best_c.val_losses[0]} -> {best_c.val_losses[best_c.val_losses.size - 1]}")
    else:
        print("Classifier did not improve")

    # As far as I'm aware this will always be the same as best_epochs, so we don't even
    # really need to track it, but at least it lets us extract it from outside this local
    # function
    print(f"Classifier trained for {best_c.trained_epochs} epochs\n")

    plot_decision_regions(x_val, t_val, best_c, path=decision_plot_path)

    # From the plotting of the losses i noticed that some of the classifiers
    # grow to get a lower loss on the validation set than the training set which
    # is somewhat unexpected though not unheard of. All the curves are monotone
    # as the loops above will always choose the best classifier after brute forcing
    # the best parameters, meaning if there is a combination where the graph is not
    # monotone there will always be a combination with fewer epochs that will stop
    # before the graph changes direction. There could theoretically be a combination
    # where the graph briefly changed in the wrong direction, but then later
    # changes back, but all these combinations would be eliminated by the early
    # stopping implemented in task 1.1e.
    plot_losses(best_c.train_losses, best_c.val_losses, path=losses_plot_path)


def test_linear_classifier_without_scaling() -> None:
    # When first running the below code with testing for epochs from 1..100 I
    # found that pretty much any training would decrease the accuracy of the
    # model. The best we could do was get the same accuracy as with an untrained
    # classifier. However after increasing the amount of epochs to 200 I finally
    # found an accuracy ever so slightly better than default. With a learning
    # rate of 0.01 and 194 epochs we can get an accuracy of 0.61.
    # (this is compared to the default value of 0.604). I ended up reverting
    # back to 100 epochs however as 200 took too long and would lead to
    # number overflow errors.

    print("Testing linear classifier without scaling")
    test_classifier(
        X_TRAIN,
        T_BINARY_TRAIN,
        X_VAL,
        T_BINARY_VAL,
        "assets/linear-without-scaling.png",
        "assets/linear-without-scaling-losses.png",
        LinearRegressionClassifier,
    )


def test_linear_classifier_with_scaling() -> None:
    # The optimal parameters for the linear classifier scaled with the standard
    # scaler are 9 epochs with a learning rate of 0.3 resulting in an accuracy
    # of 0.762, and for the minmax scaler its 66 epochs and a learning rate of
    # 0.5 resulting in an accuracy of 0.708. Both are significant improvements
    # compared to the unscaled data.
    #
    # NOTE: I also noticed that by modifying the threshold of the predict
    # function of the classifier we could further increase the accuracy on the
    # standard scaled data. Here i found that ~0.45 would be the optimal 
    # resulting in an accuracy of 0.79. Though this is definetly specific to
    # this test data so i left it out from the definition of the classifier.

    print("Testing linear classifier with standard scaling")
    test_classifier(
        standard_scaler(X_TRAIN),
        T_BINARY_TRAIN,
        standard_scaler(X_VAL),
        T_BINARY_VAL,
        "assets/linear-standard-scaling.png",
        "assets/linear-standard-scaling-losses.png",
        LinearRegressionClassifier,
    )

    print("Testing linear classifier with minmax scaler")
    test_classifier(
        minmax_scaler(X_TRAIN),
        T_BINARY_TRAIN,
        minmax_scaler(X_VAL),
        T_BINARY_VAL,
        "assets/linear-minmax-scaling.png",
        "assets/linear-minmax-scaling-losses.png",
        LinearRegressionClassifier,
    )


def test_logistic_classifier() -> None:
    # For the logistic regression classifier we find the optimal paramters to be
    # 104 epochs with a learning rate of 0.5 resulting in an accuracy of 0.766

    print("Testing logistic classifier with standard scaling")
    test_classifier(
        standard_scaler(X_TRAIN),
        T_BINARY_TRAIN,
        standard_scaler(X_VAL),
        T_BINARY_VAL,
        "assets/logistic.png",
        "assets/logistic-losses.png",
        LogisticRegressionClassifier,
    )


def test_multi_logistic_classifier() -> None:
    print("Testing multi class logistic classifier with standard scaling")

    test_classifier(
        standard_scaler(X_TRAIN),
        T_MULTI_TRAIN,
        standard_scaler(X_VAL),
        T_MULTI_VAL,
        "assets/logistic-multi.png",
        "assets/logistic-mutli-losses.png",
        MultiLogisticRegressionClassifier,
    )


def main() -> None:
    # test_linear_classifier_without_scaling()
    # test_linear_classifier_with_scaling()
    # test_logistic_classifier()
    test_multi_logistic_classifier()

    # plot_training_set(X_TRAIN, T_MULTI_TRAIN, "Multi-class set", "assets/multi-class.png")
    # plot_training_set(X_TRAIN, T_BINARY_TRAIN, "Binary set", "assets/binary.png")

if __name__ == "__main__":
    main()
